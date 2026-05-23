import os
import re
import math
import requests
import Levenshtein
from bs4 import BeautifulSoup
from markitdown import MarkItDown
from database import get_db


try:
    from pdf2image import convert_from_path
    import pytesseract
except ImportError:
    print("Aviso: pdf2image o pytesseract no estan instalados. El OCR de respaldo no funcionara.")

def calcular_similitud_levenshtein(texto_buscado, texto_bloque):
    if not texto_buscado and not texto_bloque:
        return 1.000
    if not texto_buscado or not texto_bloque:
        return 0.000
    ratio = Levenshtein.ratio(texto_buscado.lower(), texto_bloque.lower())
    factor = 1000
    similitud_truncada = math.trunc(ratio * factor) 
    return float(similitud_truncada)

def extraer_anio_de_texto(texto, url_origen):
    texto_seguro = (texto or "") + " " + (url_origen or "")
    anios = re.findall(r'\b(20[0-2][0-9])\b', texto_seguro)
    for anio in anios:
        return int(anio) 
    return 2026  

def ejecutar_ocr_respaldo(pdf_path):
    try:
        paginas = convert_from_path(pdf_path, 130)  
        texto_extraido = ""
        for pagina in paginas:
            texto_extraido += pytesseract.image_to_string(pagina, lang='es') + "\n"
        return texto_extraido
    except Exception as e:
        print(f"Error procesando OCR en {pdf_path}: {e}")
        return ""

def ejecutar_scraping_url(source_id, url_origen):
    
    download_path = "downloaded_pdfs"
    os.makedirs(download_path, exist_ok=True)
    try:
        res = requests.get(url_origen, timeout=10)
        res.raise_for_status()
        html = res.text
    except Exception as e:
        print(f"Error al conectar con la URL {url_origen}: {e}")
        return

    soup = BeautifulSoup(html, 'html.parser')
    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.pdf'):
            if not href.startswith('http'):
                from urllib.parse import urljoin
                href = urljoin(url_origen, href)
            pdf_links.append(href)

    converter = MarkItDown()
    with get_db() as conn:
        for link in pdf_links:
            filename = link.split('/')[-1]
            existe = conn.execute('''
                SELECT id FROM documents 
                WHERE source_id = ? AND filename = ?
            ''', (source_id, filename)).fetchone()
            if existe:
                print(f" El archivo {filename} ya esta indexado. Saltando")
                continue  
            downloaded_file = os.path.join(download_path, filename)
            try:
                pdf_res = requests.get(link, timeout=10)
                pdf_res.raise_for_status()
                with open(downloaded_file, 'wb') as f:
                    f.write(pdf_res.content)
            except Exception as e:
                print(f"Error descargando {link}: {e}")
                continue
            content = ""
            try:
                result = converter.convert(downloaded_file)
                content = result.markdown or result.text_content or ""
            except Exception as e:
                print(f"Error con MarkItDown en {filename}: {e}")
            if len(content.strip()) < 40:
                print(f" {filename} parece no tener texto digital. Ejecutando OCR")
                content = ejecutar_ocr_respaldo(downloaded_file)
            word_count = len(content.split())
            year = extraer_anio_de_texto(content, link)
            conn.execute('''
                INSERT INTO documents (source_id, filename, original_url, year, content, word_count)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (source_id, filename, link, year, content, word_count))
            
        conn.execute('UPDATE sources SET status = "scrappeada" WHERE id = ?', (source_id,))
        conn.commit()
import os
import re
import math
import requests
import Levenshtein
from bs4 import BeautifulSoup
from markitdown import MarkItDown
from database import get_db

# Soporte para el Extra de OCR
try:
    from pdf2image import convert_from_path
    import pytesseract
except ImportError:
    print("Aviso: pdf2image o pytesseract no están instalados. El OCR de respaldo no funcionará.")

def calcular_similitud_levenshtein(texto_buscado, texto_bloque):
    """
    Calcula el ratio de Levenshtein.
    Corta el resultado estrictamente a 3 decimales sin aplicar redondeo.
    Devuelve un valor de tipo float para operaciones lógicas.
    """
    if not texto_buscado and not texto_bloque:
        return 1.000
    if not texto_buscado or not texto_bloque:
        return 0.000
        
    ratio = Levenshtein.ratio(texto_buscado.lower(), texto_bloque.lower())
    
    # Truncado estricto eliminando decimales sobrantes sin redondear
    factor = 1000
    similitud_truncada = math.trunc(ratio * factor) / factor
    return float(similitud_truncada)

def extraer_anio_de_texto(texto, url_origen):
    """Busca patrones de años (2000 a 2029) en el texto o en la misma URL del archivo."""
    texto_seguro = (texto or "") + " " + (url_origen or "")
    anios = re.findall(r'\b(20[0-2][0-9])\b', texto_seguro)
    
    # Recorremos la lista. Si tiene elementos, tomamos el primero que encuentre
    for anio in anios:
        return int(anio)
        
    return 2026  # Año por defecto si no encuentra nada

def ejecutar_ocr_respaldo(pdf_path):
    """Extrae texto usando OCR mediante pytesseract si MarkItDown no obtuvo caracteres."""
    try:
        paginas = convert_from_path(pdf_path, 130)  # Resolución equilibrada para velocidad
        texto_extraido = ""
        for pagina in paginas:
            texto_extraido += pytesseract.image_to_string(pagina, lang='es') + "\n"
        return texto_extraido
    except Exception as e:
        print(f"Error procesando OCR en {pdf_path}: {e}")
        return ""

def ejecutar_scraping_url(source_id, url_origen):
    """
    Descarga, convierte a markdown (o aplica OCR si es imagen) e indexa 
    los archivos de la URL origen en la base de datos.
    """
    download_path = "downloaded_pdfs"
    os.makedirs(download_path, exist_ok=True)
    
    # 1. Obtener HTML de la página web
    try:
        res = requests.get(url_origen, timeout=10)
        res.raise_for_status()
        html = res.text
    except Exception as e:
        print(f"Error al conectar con la URL {url_origen}: {e}")
        return

    # 2. Extracción de enlaces de PDFs (idéntico a pdf_functions.py)
    soup = BeautifulSoup(html, 'html.parser')
    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.pdf'):
            if not href.startswith('http'):
                from urllib.parse import urljoin
                href = urljoin(url_origen, href)
            pdf_links.append(href)

    # 3. Descarga y procesamiento de cada archivo
    converter = MarkItDown()
    
    with get_db() as conn:
        for link in pdf_links:
            filename = link.split('/')[-1]
            downloaded_file = os.path.join(download_path, filename)
            
            # Descarga del archivo binario
            try:
                pdf_res = requests.get(link, timeout=10)
                pdf_res.raise_for_status()
                with open(downloaded_file, 'wb') as f:
                    f.write(pdf_res.content)
            except Exception as e:
                print(f"Error descargando {link}: {e}")
                continue
            
            # Conversión principal con MarkItDown
            content = ""
            try:
                result = converter.convert(downloaded_file)
                content = result.markdown or result.text_content or ""
            except Exception as e:
                print(f"Error con MarkItDown en {filename}: {e}")
            
            # [EXTRA OCR]: Si viene vacío o es un renderizado de imagen escaneada
            if len(content.strip()) < 40:
                print(f"⚠️ {filename} parece no tener texto digital. Ejecutando OCR...")
                content = ejecutar_ocr_respaldo(downloaded_file)
            
            # Cálculo de metadatos para el Home
            word_count = len(content.split())
            year = extraer_anio_de_texto(content, link)
            
            # Guardado indexado en base de datos
            conn.execute('''
                INSERT INTO documents (source_id, filename, original_url, year, content, word_count)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (source_id, filename, link, year, content, word_count))
            
        # Finalizar marcando la URL base como procesada
        conn.execute('UPDATE sources SET status = "scrappeada" WHERE id = ?', (source_id,))
        conn.commit()
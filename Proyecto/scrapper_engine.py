import re
import math
from database import get_db

def calcular_levenshtein_distance(s1, s2):
    """Calcula la distancia de Levenshtein estándar."""
    if len(s1) < len(s2):
        return calcular_levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
        
    return previous_row[-1]

def calcular_similitud_levenshtein(texto_buscado, texto_bloque):
    """Retorna el porcentaje de similitud truncado a 3 decimales sin redondear."""
    if not texto_buscado and not texto_bloque:
        return 1.000
    if not texto_buscado or not texto_bloque:
        return 0.000
        
    distancia = calcular_levenshtein_distance(texto_buscado, texto_bloque)
    max_len = max(len(texto_buscado), len(texto_bloque))
    similitud = 1.0 - (distancia / max_len)
    
    # Truncado estricto a 3 decimales sin redondeo (ej. 0.8569 -> 0.856)
    factor = 1000
    similitud_truncada = math.trunc(similitud * factor) / factor
    return similitud_truncada

def ejecutar_scraping_url(source_id, url):
    """
    Aquí integrarán el código del repositorio base para descargar PDFs.
    Simulación de la integración de OCR si el PDF no tiene texto:
    """
    # 1. Descargar PDFs de la URL...
    # 2. Extraer texto digital. Si viene vacío:
    #    text = pytesseract.image_to_string(pdf_page_render) [OCR EXTRA]
    
    # Mock de inserción para pruebas del sistema web:
    filename = "documento_ejemplo.pdf"
    content = "Este es un bloque de texto indexado para pruebas de desarrollo de sistemas de información."
    word_count = len(content.split())
    year = 2026
    
    with get_db() as conn:
        conn.execute('''
            INSERT INTO documents (source_id, filename, original_url, year, content, word_count)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (source_id, filename, url + "/" + filename, year, content, word_count))
        
        conn.execute('UPDATE sources SET status = "scrappeada" WHERE id = ?', (source_id,))
        conn.commit()
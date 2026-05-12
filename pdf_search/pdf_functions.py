import requests
from bs4 import BeautifulSoup
import os

def get_webpage(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None
    
def extract_pdf_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.pdf'):
            pdf_links.append(href)
    return pdf_links
    
if __name__ == "__main__":
    url = "https://fi-ing.unison.mx/acuerdos-de-sesiones-del-h-colegio-de-la-facultad-interdisciplinaria-de-ingenieria-2026/"
    html = get_webpage(url)
    pdf_links = extract_pdf_links(html)
    for link in pdf_links:
        print(link)
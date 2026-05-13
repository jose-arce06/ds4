""" PDF functions for searching and processing PDF files from a webpage. """
from markitdown import MarkItDown
import requests
from bs4 import BeautifulSoup
import os 

def get_webpage(url):
    """ Fetches the content of a webpage given its URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check if the request was successful
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None 
    
def extract_pdf_links(html):
    """ Parses the HTML content and extracts all PDF links."""
    soup = BeautifulSoup(html, 'html.parser')
    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.pdf'):
            pdf_links.append(href)
    return pdf_links

def download_pdf(url, filename):
    """ Downloads a PDF file from a given URL and saves it with a specified filename."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the PDF: {e}")

def get_pdfs(url = "https://fi-ing.unison.mx/acuerdos-de-sesiones-del-h-colegio-de-la-facultad-interdisciplinaria-de-ingenieria-2026/"):
    """ Main function to orchestrate the PDF downloading process."""
    
    download_path = "downloaded_pdfs"
    if not os.path.exists(download_path):
        # Create the directory if it doesn't exist
        os.makedirs(download_path, exist_ok=True)
    html = get_webpage(url)
    if not html:
        print(f"Failed to fetch the webpage: {url}")
        exit(1)
    pdf_links = extract_pdf_links(html)
    for link in pdf_links:
        print(link)
        filename = link.split('/')[-1]
        downloaded_file = os.path.join(download_path, filename) 
        download_pdf(link, f"{downloaded_file}")
        print(f"Downloaded: {downloaded_file}")

def convert_pdf_to_markdown(pdf_path, markdown_path):
    """ Converts a PDF file to Markdown format using MarkItDown."""
    try:
        converter = MarkItDown()
        result = converter.convert(pdf_path)
        markdown_content = result.markdown or result.text_content
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
    except Exception as e:
        print(f"Error converting PDF to Markdown: {e}")

def main():
    """ Main function to orchestrate the PDF downloading process."""
    #get_pdfs()
    if not os.path.exists("markdown_files"):
        os.makedirs("markdown_files", exist_ok=True)
    for filename in os.listdir("downloaded_pdfs"):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join("downloaded_pdfs", filename)
            markdown_path = os.path.join("markdown_files", f"{os.path.splitext(filename)[0]}.md")
            convert_pdf_to_markdown(pdf_path, markdown_path)
            print(f"Converted {pdf_path} to {markdown_path}")

if  __name__ == "__main__":
    main()
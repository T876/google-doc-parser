"""
Google Doc Parser

Fetches Google Doc content using requests and cleans up the data. It then builds a 2D map of nodes and prints it to the console,
filling in the blanks with space characters.

"""

import requests
import re
from bs4 import BeautifulSoup

def extract_document_id(url: str) -> str:
    """
    Extracts the document ID from a Google Docs URL.
    """
    doc_id_match = re.search(r'/document/d/(?:e/)?([a-zA-Z0-9-_]+)', url)
    if not doc_id_match:
        raise ValueError("Invalid Google Doc URL. Please provide a valid Google Docs URL.")
    
    doc_id = doc_id_match.group(1)
    return doc_id


def get_google_doc_html(url: str) -> str:
    """
    Fetches the HTML content of a published Google Doc.
    """
    doc_id = extract_document_id(url)
    
    # Try different approaches for different URL types (my demo vs. provided doc)
    urls_to_try = [
        f"https://docs.google.com/document/d/e/{doc_id}/pub",
        f"https://docs.google.com/document/d/{doc_id}/pub",
        f"https://docs.google.com/document/d/{doc_id}/export?format=html",
    ]
    
    for attempt_url in urls_to_try:
        try:
            response = requests.get(attempt_url, timeout=30)
            if response.status_code == 200:
                print("Document contents fetched successfully.")
                return response.text
        except requests.RequestException as e:
            pass
    
    raise Exception("Could not fetch document from any URL format")


def clean_document_content(html_content: str) -> str:
    """
    Extracts clean text content from the HTML.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # We don't need this stuff
    for script in soup(["script", "style"]):
        script.decompose()
    
    main_content = soup.find('body')
    
    if not main_content:
        raise Exception("Could not find main content")
    
    text = main_content.get_text(separator='\n', strip=True)
    lines = text.split('\n')
    
    return [line for line in lines if line.strip()]

def build_nodes_from_rows(rows: list[str]) -> tuple[dict, int, int]:
    """
    Builds a 2D map of nodes from the data in the provided document.
    """
    nodes = {}
    reached_data = False
    i = 0
    max_x = 0
    max_y = 0
    
    while i < len(rows):
        if reached_data:
            if i + 2 < len(rows):
                x = int(rows[i])
                y = int(rows[i+2])
                char = rows[i+1]
                
                if y not in nodes:
                    nodes[y] = {}
                nodes[y][x] = char
                max_x = max(max_x, x)
                max_y = max(max_y, y)
                i += 3
            else:
                break
        else:
            if rows[i] == "y-coordinate":
                reached_data = True
            i += 1
    
    return nodes, max_x, max_y

def print_node_map(nodes: dict, max_x: int, max_y: int):
    """
    Prints the 2D node map to the console.
    """
    for y in reversed(range(max_y + 1)):
        for x in range(max_x + 1):
            if x in nodes[y]:
                print(nodes[y][x], end="")
            else:
                print(" ", end="")
        print()

def main():
    """
    Main function - get URL and fetch clean document content. Then, decode the message and print it.
    """
    print("Google Doc Content Fetcher")
    print("=" * 40)
    
    url = input("Enter the Google Doc URL: ").strip()
    
    if not url:
        print("No URL provided. Exiting.")
        return
    
    try:
        print("\nFetching document...")
        html_content = get_google_doc_html(url)
        
        print("Cleaning content...")
        clean_rows = clean_document_content(html_content)
        
        nodes, max_x, max_y = build_nodes_from_rows(clean_rows)

        print("\nMessage:\n")
        print_node_map(nodes, max_x, max_y)
        print("\n" * 2);
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

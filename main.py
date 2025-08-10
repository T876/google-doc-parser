#!/usr/bin/env python3
"""
Google Doc Parser - Simple Requests Approach

Fetches Google Doc content using requests and cleans up the data.
"""

import requests
import re
from bs4 import BeautifulSoup

def extract_document_id(url: str) -> str:
    """
    Extracts the document ID from a Google Docs URL.
    """
    print(f"Original URL: {url}")
    
    # Handle both regular URLs (/d/DOC_ID) and published URLs (/d/e/DOC_ID)
    doc_id_match = re.search(r'/document/d/(?:e/)?([a-zA-Z0-9-_]+)', url)
    if not doc_id_match:
        raise ValueError("Invalid Google Doc URL. Please provide a valid Google Docs URL.")
    
    doc_id = doc_id_match.group(1)
    print(f"Document ID: {doc_id}")
    return doc_id


def get_google_doc_html(url: str) -> str:
    """
    Fetches the HTML content of a published Google Doc.
    """
    doc_id = extract_document_id(url)
    
    # Try different approaches for different URL types
    urls_to_try = [
        f"https://docs.google.com/document/d/e/{doc_id}/pub",  # Published format
        f"https://docs.google.com/document/d/{doc_id}/pub",    # Regular format
        f"https://docs.google.com/document/d/{doc_id}/export?format=html",  # HTML export
    ]
    
    for attempt_url in urls_to_try:
        print(f"Trying: {attempt_url}")
        try:
            response = requests.get(attempt_url, timeout=30)
            if response.status_code == 200:
                print(f"Success! Retrieved {len(response.text)} characters")
                return response.text
            else:
                print(f"Failed with status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Request failed: {e}")
    
    raise Exception("Could not fetch document from any URL format")


def clean_document_content(html_content: str) -> str:
    """
    Extracts clean text content from the HTML.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # We don't need this stuff
    for script in soup(["script", "style"]):
        script.decompose()
    
    content_areas = [
        soup.find('div', {'id': 'contents'}),
        soup.find('div', {'class': 'doc-content'}),
        soup.find('div', {'class': 'kix-appview-editor'}),
        soup.find('body')  # fallback
    ]
    
    main_content = None
    for area in content_areas:
        if area:
            main_content = area
            break
    
    if not main_content:
        main_content = soup
    
    text = main_content.get_text(separator='\n', strip=True)
    lines = text.split('\n')
    
    return [line for line in lines if line.strip()]

def build_nodes_from_rows(rows: list[str]) -> tuple[dict, int, int]:
    nodes = {} # 2D map of nodes
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
    for y in reversed(range(max_y + 1)):
        for x in range(max_x + 1):
            if x in nodes[y]:
                print(nodes[y][x], end="")
            else:
                print(" ", end="")
        print()

def main():
    """
    Main function - get URL and fetch clean document content.
    """
    print("Google Doc Content Fetcher")
    print("=" * 40)
    
    # Get the URL from user
    url = input("Enter the Google Doc URL: ").strip()
    
    if not url:
        print("No URL provided. Exiting.")
        return
    
    try:
        # Fetch the HTML content
        print("\nFetching document...")
        html_content = get_google_doc_html(url)
        
        # Clean and extract the content
        print("Cleaning content...")
        clean_rows = clean_document_content(html_content)
        
        nodes, max_x, max_y = build_nodes_from_rows(clean_rows)

        print_node_map(nodes, max_x, max_y)
        print(f"Max X: {max_x}, Max Y: {max_y}")

        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

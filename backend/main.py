import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    
def extract_headlines(html):
    soup = BeautifulSoup(html, 'html.parser')
    headline_tags = ['h2', 'h3']

    seen = set()
    headlines = []

    # For getting the main h1 tag first
    h1 = soup.find('h1')
    if h1:
        text = h1.get_text(strip= True)
        if text and text not in seen:
            headlines.append(('H1', text))
            seen.add(text)

    # For getting all h2 and h3 tags in their natural order
    for tag in soup.find_all(headline_tags):
        text = tag.get_text(strip= True)
        if text and text not in seen:
            headlines.append((tag.name.upper(), text))
            seen.add(text)
        
    return headlines

def main():
    url = input("Enter a news or article page URL:").strip()
    html = fetch_html(url)

    if not html:
        return
    
    print(f"\nExtracting headlines from: {urlparse(url).netloc}")
    headlines = extract_headlines(html)

    if not headlines:
        print("No headlines found.")
        return
    
    for i, (tag, text) in enumerate(headlines, 1):
        indent = "  " * (int(tag[1]) - 1)  # Implementing indentation of 2 spaces per level to define hierarchy
        print(f"{i}. {indent}[{tag}] {text}")

if __name__ == "__main__":
    main()
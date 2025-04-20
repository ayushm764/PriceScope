import re
import requests
from bs4 import BeautifulSoup
import json
import sys

def extract_title_price_from_text(text):
    """
    Fallback: try to extract title and price from the element's text.
    Assumes the price pattern starts with the rupee symbol.
    """
    price_match = re.search(r'(₹[\d,]+)', text)
    if price_match:
        price = price_match.group(1)
        title = text[:price_match.start()].strip()
        return title, price
    return None, None

def fetch_flipkart_products(query):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        )
    }

    url = f"https://www.flipkart.com/search?q={query.replace(' ', '+')}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    products = []
    product_cards = soup.find_all("a", href=True)
    title_classes = ["KzDlHZ", "wjcEIp", "jfJfIF", "V3A3P", "IRpwTa", "s1Q9rs"]
    price_classes = ["Nx9bqj", "nWob9", "DWN0x", "_30jeq3", "price-tag"]

    for a_tag in product_cards:
        href = a_tag.get("href", "")
        if href.startswith("/search") or not ("/p/" in href or "/product/" in href or "/itm" in href):
            continue
        
        full_link = "https://www.flipkart.com" + href

        title_candidate = None
        for cls in title_classes:
            t_tag = a_tag.find("div", class_=cls) or a_tag.find("span", class_=cls)
            if t_tag:
                title_candidate = t_tag.get_text(strip=True)
                break
        
        # Fallback: try image alt attribute if title not found
        if not title_candidate:
            img = a_tag.find("img", alt=True)
            if img and img.get("alt"):
                title_candidate = img.get("alt").strip()
        
        price_candidate = None
        for cls in price_classes:
            p_tag = a_tag.find("div", class_=cls) or a_tag.find("span", class_=cls)
            if p_tag:
                price_candidate = p_tag.get_text(strip=True)
                break

        # Fallback: parse the full text for a rupee price if needed.
        if not title_candidate or not price_candidate:
            full_text = a_tag.get_text(" ", strip=True)
            title_from_text, price_from_text = extract_title_price_from_text(full_text)
            if not title_candidate:
                title_candidate = title_from_text
            if not price_candidate:
                price_candidate = price_from_text
        
        # Append product only if both title and price were found.
        if title_candidate and price_candidate:
            products.append({
                "title": title_candidate,
                "price": price_candidate,
                "link": full_link
            })
    
    return products

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "pen"
    product_data = fetch_flipkart_products(query)
    
    # Save the results to deals2.json without printing to console.
    with open("deals2.json", "w", encoding="utf-8") as f:
        json.dump(product_data, f, indent=4, ensure_ascii=False)

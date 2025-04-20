import sys
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_amazon_selenium(search_query):
    base_url = "https://www.amazon.in"
    search_url = f"{base_url}/s?k={search_query}"
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    )
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(search_url)

        wait = WebDriverWait(driver, 15)  # Reduced wait time
        wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@data-component-type="s-search-result"]')
        ))

        for _ in range(2):  # Fewer scrolls
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(1)  # Reduced wait

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        products = soup.find_all("div", {"data-component-type": "s-search-result"})
        print("Number of product containers found:", len(products))
        
        data = []
        for product in products:
            title_tag = product.select_one("a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal span")
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            
            price_symbol = product.select_one('span[aria-hidden="true"] span.a-price-symbol')
            price_whole = product.select_one('span[aria-hidden="true"] span.a-price-whole')
            if not (price_symbol and price_whole):
                continue
            price = price_symbol.get_text(strip=True) + price_whole.get_text(strip=True)
            
            link_tag = product.select_one("a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal")
            if link_tag and link_tag.get("href"):
                relative_link = link_tag.get("href")
                product_link = base_url + relative_link if relative_link.startswith('/') else relative_link
            else:
                continue
            
            data.append({
                "title": title,
                "price": price,
                "link": product_link
            })
            # Removed per-product sleep to speed up

        # Faster deduplication
        seen = set()
        unique_data = []
        for item in data:
            key = (item['title'], item['price'], item['link'])
            if key not in seen:
                seen.add(key)
                unique_data.append(item)
        
        with open("deals.json", "w", encoding="utf-8") as f:
            json.dump(unique_data, f, ensure_ascii=False, indent=4)
        
        print(f"Scraped {len(unique_data)} products for '{search_query}' and saved results to deals.json.")
    
    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    search_query = sys.argv[1] if len(sys.argv) > 1 else "iphone"
    scrape_amazon_selenium(search_query)

import json
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def format_inr(amount):
    s = str(amount)
    last_three = s[-3:]
    rest = s[:-3]
    if rest != "":
        rest = list(rest)
        rest.reverse()
        parts = []
        for i in range(0, len(rest), 2):
            part = rest[i]
            if i + 1 < len(rest):
                part += rest[i + 1]
            parts.append(part[::-1])
        formatted_rest = ','.join(parts[::-1])
        return "₹" + formatted_rest + "," + last_three
    else:
        return "₹" + last_three

def fetch_jiomart_products(query):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f"https://www.jiomart.com/search/{query.replace(' ', '%20')}"
    driver.get(url)
    time.sleep(5)

    products = []
    items = driver.find_elements(By.CSS_SELECTOR, "li.ais-InfiniteHits-item")

    for item in items:
        try:
            title_element = item.find_element(By.CSS_SELECTOR, "div.plp-card-details-name")
            price_element = item.find_element(By.CSS_SELECTOR, "span.jm-heading-xxs.jm-mb-xxs")
            link_element = item.find_element(By.TAG_NAME, "a")

            title = title_element.text.strip()
            price_raw = price_element.text.strip()
            link = link_element.get_attribute("href")

            price_clean = ''.join(c for c in price_raw if c.isdigit() or c == '.')
            if price_clean:
                price_float = float(price_clean)
                price_int = int(price_float)
                formatted_price = format_inr(price_int)  # ✅ Format properly

                products.append({
                    "title": title,
                    "price": formatted_price, 
                    "link": link
                })
        except Exception:
            continue

    driver.quit()
    return products

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "iphone"
    data = fetch_jiomart_products(query)

    with open("deals3.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✅ Scraped {len(data)} products. Saved to jiomart_deals.json")
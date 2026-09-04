import time
import os
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)
driver.get("https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart")

results = []
time.sleep(5)

search_items = driver.find_elements(By.CSS_SELECTOR, "li.cp-search-result-item")
print(f"Found {len(search_items)} search result items on the current page.")



for index, item in enumerate(search_items, start=1):
    try:
        # --- Title ---
        # Look for title span/link inside the title header
        title_element = item.find_element(By.CSS_SELECTOR, ".title-content")
        title_text = title_element.text.strip()
        
    except Exception:
        title_text = "N/A"


    try:
        # --- Authors ---
        # Find all author link elements inside the item
        author_elements = item.find_elements(By.CSS_SELECTOR, "a.author-link")
        author_names = [author.text.strip() for author in author_elements if author.text.strip()]
        
        # Join multiple authors with a semicolon
        author_text = "; ".join(author_names) if author_names else "N/A"
        
    except Exception:
        author_text = "N/A"


    try:
        # --- Format & Year ---
        # Find the div/container storing format and publication info, then retrieve the text
        format_div = item.find_element(By.CSS_SELECTOR, "div.cp-format-info, [data-test-id='format-info']")
        format_span = format_div.find_element(By.CSS_SELECTOR, "span.display-info-primary")
        format_year_text = format_span.text.strip()
        
    except Exception:
        format_year_text = "N/A"


    print(f"[{index}] Title: {title_text} | Author(s): {author_text} | Format-Year: {format_year_text}")

    record = {
        "Title": title_text,
        "Author": author_text,
        "Format-Year": format_year_text
    }
    results.append(record)



driver.quit()

# Create DataFrame and display
df = pd.DataFrame(results)
print("\n--- Final Dataframe Output ---")
print(df)

# Write DataFrame to assignment8/get_books.csv
csv_path = os.path.join("assignment8/get_books.csv")
df.to_csv(csv_path, index=False)
print(f"Successfully saved CSV file to: '{csv_path}'")

json_path = os.path.join("assignment8/get_books.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)
print(f"Successfully saved JSON file to: '{json_path}'")





# For Further Thought   : 
# Locate the pagination controls at the bottom of the page .
#  Wrap the extraction logic in a while  loop that continues executing until the "Next" button is disabled 
# Handle Pagination via URL Parameters: Alternatively, observe how BiblioCommons modifies query strings 
# (e.g., &page=2, &page=3). You can extract the total page count from the header UI (e.g., "Page 1 of 12") 
# and loop over range(1, total_pages + 1)


#  2. How to implement pagination responsibly?

#Include time.sleep(3) (or longer) between page visits to avoid sending rapid HTTP requests that mimic a Denial-of-Service (DoS) attack.

#Respect Crawl-delay: Adhere strictly to any time delays specified in the library's robots.txt file.
import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


output_dir = os.path.join("python_homework", "assignment8")
os.makedirs(output_dir, exist_ok=True)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)
wait = WebDriverWait(driver, 15)

try:
    # Step 1: Navigate to OWASP project page
    main_url = "https://owasp.org/www-project-top-ten/"
    print(f"Navigating to initial page: {main_url}")
    driver.get(main_url)

    # Step 2: Flexible XPath targeting the OWASP Top Ten version link inside sec-main
    # This targets <a> tags inside #sec-main containing 'Top Ten' or 'Top 10' in text or href
    link_xpath = "//section[@id='sec-main']//a[contains(translate(text(), 'T', 't'), 'top') and (contains(text(), '10') or contains(translate(text(), 'T', 't'), 'ten'))]"



    
    try:
        # Wait until present in DOM
        target_link = wait.until(EC.presence_of_element_located((By.XPATH, link_xpath)))
        href = target_link.get_attribute("href")
        print(f"Found link: '{target_link.text.strip()}' -> {href}")
        
        # Scroll element into view before clicking
        driver.execute_script("arguments[0].scrollIntoView(true);", target_link)
        
        # Click via JavaScript to avoid click interception issues in headless mode
        driver.execute_script("arguments[0].click();", target_link)
    except Exception as e:
        print(f"Click failed or timed out: {e}. Navigating directly to Top 10 page...")
        driver.get("https://owasp.org/Top10/")

    # Step 3: Extract vulnerabilities on the target page
    # Look for any ordered list (<ol>) or unordered list (<ul>) containing top 10 items
    wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
    
    # XPath for top 10 list items (checking for list items under sec-main or specific headers)
    vulnerability_xpath = "//section[@id='sec-main']//li/a | //ol/li/a[contains(text(), 'A0') or contains(text(), 'A10') or contains(text(), 'A1')]"
    
    elements = driver.find_elements(By.XPATH, vulnerability_xpath)
    
    top_10_list = []
    seen_titles = set()

    for elem in elements:
        title = elem.text.strip()
        link = elem.get_attribute("href")
        
        if title and link and title not in seen_titles:
            # Clean up title whitespace
            clean_title = " ".join(title.split())
            seen_titles.add(title)
            top_10_list.append({"title": clean_title, "href": link})
            
            if len(top_10_list) == 10:
                break

    # If list is empty, fallback to searching all A-prefixed vulnerability links
    if not top_10_list:
        all_links = driver.find_elements(By.XPATH, "//a[starts-with(normalize-space(text()), 'A0') or starts-with(normalize-space(text()), 'A10')]")
        for elem in all_links:
            title = elem.text.strip()
            link = elem.get_attribute("href")
            if title and link and title not in seen_titles:
                seen_titles.add(title)
                top_10_list.append({"title": " ".join(title.split()), "href": link})
            if len(top_10_list) == 10:
                break

    # Print results
    print(f"\nSuccessfully extracted {len(top_10_list)} vulnerabilities:")
    for idx, item in enumerate(top_10_list, 1):
        print(f"{idx}. {item['title']} - {item['href']}")

    # Save to CSV
    csv_file_path = os.path.join("assignment8/owasp_top_10.csv")
    with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "href"])
        writer.writeheader()
        writer.writerows(top_10_list)

    print(f"\nData saved to {csv_file_path}")

finally:
    driver.quit()
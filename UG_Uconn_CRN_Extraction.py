from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
import pandas as pd
driver = webdriver.Chrome()

try:
    driver.get("https://catalog.uconn.edu/course-search/?details&code")
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "crit-coursetype")))
    
    select_element = driver.find_element(By.ID, "crit-coursetype")
    select = Select(select_element)
    
    select.select_by_visible_text("Undergraduate")
    
    search_button = driver.find_element(By.ID, "search-button")
    time.sleep(5)
    search_button.click()
    time.sleep(10)
    

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    time.sleep(10)
    print(soup.prettify())
    api_payload = []
    course_links = soup.find_all("a",href=True,class_="result__link")

    for link in course_links:
        course_code = link.find('span', class_='result__code').text.strip()
        
        course_title = link.find('span', class_='result__title').text.strip()
        
        data_matched = link.get('data-matched', '').strip() 
        data_matched  = list(data_matched.split(","))[0]
        data_srcdb = link.get('data-srcdb', '').strip() 
        
        print(f"Course Code: {course_code}")
        print(f"Course Title: {course_title}")
        print(f"CRN: {data_matched}")
        print(f"Source DB: {data_srcdb}")
        print("-" * 50)
        api_payload.append([course_code,data_matched, data_srcdb])
    api_payload = pd.DataFrame(api_payload, columns=['Course_Code', 'CRN', 'Source_DB'])
    api_payload.to_csv('UG_Uconn_CRN.csv', index=False)
    
    
except Exception as e:
    print(e)

finally:
    driver.quit()

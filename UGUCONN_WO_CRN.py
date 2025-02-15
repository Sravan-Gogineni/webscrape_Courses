from bs4 import BeautifulSoup
import requests
import pandas as pd 

url = 'https://catalog.uconn.edu/undergraduate/courses/'
response = requests.get(url)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')


course_list = soup.find('ul', class_="nav leveltwo", id="/undergraduate/courses/")

course_links = []
for li in course_list.find_all('li'):
    links = li.find_all('a', href=True)
    
    for link in links:
        course_links.append(link['href'])
course_list = []
for link in course_links:
    link = "https://catalog.uconn.edu" + link
    print("Scraping: ", link)
    response = requests.get(link)
    print(response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    course_codes = soup.find_all('span', class_='detail-code') 
    course_title = soup.find_all('span', class_='detail-title')
    course_credits = soup.find_all('span', class_='detail-hours_html')
    
    for code, title, credits in zip(course_codes, course_title, course_credits):
        course_code = code.get_text(strip=True)
        course_title = title.get_text(strip=True)
        course_credit = credits.get_text(strip=True)
        
        course_list.append([course_code, course_title, course_credit])


df = pd.DataFrame(course_list, columns=['Course_Code', 'Course_Title', 'Course_Credit'])

df.to_csv('UG_UCONN_NO_CRN.csv', index=False)
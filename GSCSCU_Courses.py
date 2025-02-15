from bs4 import BeautifulSoup
import requests
import pandas as pd 

url = 'https://catalog.southernct.edu/graduate/courses.html'

response = requests.get(url)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
df_list = []
course_box = soup.find_all('div', class_='course-box')
for course in course_box:
    course_title = course.find('h2').text
    df_list.append(course_title)

    

df_dict = {'graduate_Course_Title': df_list}
df = pd.DataFrame(df_dict)
print(df)

df.to_csv('graduate_course_catalog_SCSU.csv', index=False)
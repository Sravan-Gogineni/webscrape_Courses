from bs4 import BeautifulSoup
import requests
import pandas as pd 

url = 'https://catalog.southernct.edu/undergraduate/courses.html'

response = requests.get(url,verify=False)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
course_list = []
credit_list = []
course_box = soup.find_all('div', class_='course-box')
for course in course_box:
    course_title = course.find('h2').text
    course_list.append(course_title)
    credit = course.find('p', class_='course-credits' ).text
    credit_list.append(credit)

    
    

df_dict = {'Undergrad_Course_Title': course_list, 'Credit': credit_list}
df = pd.DataFrame(df_dict)
print(df)

df.to_csv('UG_SCSU_Courses.csv', index=False)
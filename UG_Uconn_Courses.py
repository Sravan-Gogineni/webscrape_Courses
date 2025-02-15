import requests
import json
import pandas as pd
df = pd.read_csv('UG_Uconn_CRN.csv')

url = "https://catalog.uconn.edu/course-search/api/?page=fose&route=details"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}
final_details = []
for row in df.itertuples():
    payload = {
        "group": f"code:{row.Course_Code}",
        "key": f"{row.CRN}",
        "srcdb": "1253",
        "matched": f"{row.CRN}"
    }
    print(payload)


    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        data = response.json()
        
        course_code = data['code']
        course_title = data['title']
        course_credit = data['hours_html']
        final_details.append([course_code, course_title, course_credit])
    else:
        print(f"Error: Unable to fetch course data. Status code: {response.status_code}")


print(final_details)
df = pd.DataFrame(final_details, columns=['Course_Code', 'Course_Title', 'Course_Credit'])

df.to_csv('UG_UCONN_Courses.csv', index=False)
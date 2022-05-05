import requests

import datetime
my_date = datetime.date.today() # if date is 01/01/2018
year, week_num, day_of_week = my_date.isocalendar()
print("Week #" + str(week_num) + " of year " + str(year))


import requests

url = "https://api.notion.com/v1/pages/6f47ddad26be47ae9f73e33f4619ee32"

payload = {"properties": {
            "title": {
                "title": [
                    {
                        "text": {
                            "content": "Personal Home" + " - Week #" + str(week_num)
                        }
                    }
                ]
            }        
        }}
headers = {
    "Accept": "application/json",
    "Notion-Version": "2022-02-22",
    "Content-Type": "application/json",
    "Authorization": "Bearer secret_ys8V5ie6X2czdYF8ULaN4drZyB78CllbHuGSC5kmmT0"
}

response = requests.patch(url, json=payload, headers=headers)

print(response.text)
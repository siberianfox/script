import requests
import datetime
from datetime import timezone,timedelta

utc_dt = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
china_time = utc_dt.astimezone(timezone(timedelta(hours=8)))

year, week_num, day_of_week = china_time.isocalendar()
print("Week #" + str(week_num) + " of year " + str(year))

timestr = str(china_time.month) + "/" + str(china_time.day) + " "
timestr += str(china_time.hour) + ":"
timestr += str(china_time.minute)

print(timestr)

#Post the information to notion
url = "https://api.notion.com/v1/pages/6f47ddad26be47ae9f73e33f4619ee32"

payload = {"properties": {
            "title": {
                "title": [
                    {
                        "text": {
                            "content": "Personal Home" + " - Week #" + str(week_num) + "-" + timestr
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

print(response.text.encode("utf-8", errors="ignore"))
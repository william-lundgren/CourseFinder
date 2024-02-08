import re

import requests
from bs4 import BeautifulSoup as bs

choices = """
S = SPECIAL TERM 1
T = SPECIAL TERM 2
2017_2
2017_S
2017_T
2018_1
2018_2
2018_S
2018_T
2019_1
2017_1
2019_2
2019_S
2019_T
2020_1
2020_2
2021_1
2021_2
2021_S
2021_T
2022_1
2022_2
2023_1
2023_2
"""


def func(code, year, semester, search=False, subj_code=None):
    if search == True and subj_code is not None:
        cload = "Search"
    else:
        cload = "CLoad"
        subj_code = "Enter+Keywords+or+Course+Code"

    url = "https://wis.ntu.edu.sg/webexe/owa/AUS_SUBJ_CONT.main_display1"

    payload = f"acadsem={year}_{semester}&acadsem={year}_{semester}&r_course_yr={code}&r_subj_code" \
              f"={subj_code}&boption=" \
              f"{cload}&acad={year}&semester={semester}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "sv-SE,sv;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://wis.ntu.edu.sg/",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://wis.ntu.edu.sg",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "iframe",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    #print(response.text)

    with open("output.html", "w") as file:
        file.write(response.text)

    html = response.content
    soup = bs(html, "html.parser")
    bookings = soup.body.findAll(string=re.compile('^Prerequisite:$'))
    print(bookings[0].)

with open("courses_looong.txt", "r") as file:
    code = file.readlines()[0][:-1]


if __name__ =="__main__":
    year, sem = "2023", "2"
    func(code, year, sem)


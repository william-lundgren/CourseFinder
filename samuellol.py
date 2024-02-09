import re
import time
import os
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
    print("Getting response")
    response = requests.request("POST", url, data=payload, headers=headers)
    print("Response received")
    # print(response.text)

    with open("output.html", "w") as file:
        file.write(response.text)

    html = response.content
    soup = bs(html, "html.parser")

    courses = soup.find_all("table", class_="")

    courses_txt = []
    try:
        for course in courses:

            # All the course data are in "td" tags. Always returns a list of 3 (i hope)
            check_prerequisite = course.findAll(string=re.compile('^Prerequisite:$'))
            #print(check_prerequisite)
            prerequisites = len(check_prerequisite) # != []  # prereqs exist
            # print("pre req:", prerequisite)

            course_data = course.find_all("tr")  # all tr tags are every line in each course
            # print(course_data)

            course_code, course_name, points = [element.text for element in
                                                course_data[0].findAll("td")]  # first element is always heading
            points = " ".join(points.split())  # remove leading spaces
            if prerequisites:  # TODO add fix for when there is 2 lines of prerequisits: ???????

                # TODO add a check for if it contains or, add 1:1+no of or so all prereqs are met
                all_prereqs = "" #SOMETIMES MULTIPLE ROWS OF PREREQ IDK WHY SO ADD THEM ALL TO THIS VAR
                for i in range(1, prerequisites + 1):
                    prereq_num = i
                    prerequisite_data = course_data[prereq_num].findAll("td")[1].text + " "
                    while "or" in prerequisite_data.split()[-1].lower():
                        #print(prerequisite_data)
                        prereq_num += 1
                        prerequisite_data = prerequisite_data.replace("\n", "") + " " + course_data[prereq_num].findAll("td")[1].text
    #                    prereqdata += course_datai+=1.findall("td)[1].text
                    all_prereqs += prerequisite_data
                print("All prereqs:", all_prereqs)
                    # print(prerequisite_data)
                # print(f"Code: {course_code}, Name: {course_name}, Points: {points} Prerequisite: {prerequisite_data if prerequisite else 'No Prerequisite'}")

            with open("courses.txt", "r") as output_file:
                results_text = output_file.readlines()
            if not any(f"Code: {code}" in res for res in
                       results_text):  # make sure course isnt already in document before adding, duplicates are not needed
                string_to_append = f"Code: {course_code}, Name: {course_name}, Points: {points}, Prerequisite:" \
                                   f" {all_prereqs if prerequisites else 'No Prerequisite'}\n"

                # Get rid of multiple spaces in string
                string_to_append = " ".join(string_to_append.split()) + "\n"
                courses_txt.append(string_to_append)


    except ValueError:
        with open("problems.txt", "a") as file:
            file.write(f"{code}, {year}, {semester}\n")
        return []

    return courses_txt
    # print(courses[0])


# roblem = "MLOAD%3BAHIS%3B"

def get_website_from_code(code, year=None, semester=None):
    if year is None and semester is None:
        year, semester = "2023", "2"

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
    print("Getting response")
    response = requests.request("POST", url, data=payload, headers=headers)
    print("Response received")
    with open("output.html", "w") as file:
        file.write(response.text)
    os.system("start http://localhost:63342/CourseFinder/output.html")


def main():
    start_row = 467
    with open("courses_looong.txt", "r") as file:
        course_codes = file.readlines()

    bool = True
    with open("courses.txt", "a") as output:
        for i, code in enumerate(course_codes[start_row - 1:]):  # start off where it crashed
            if bool == True:
                print(code)
                bool = False
            print(f"Starting scraping on row {start_row + i} out of {len(course_codes)}.")
            year, sem = "2023", "2"
            output.write("".join(func(code[:-1], year, sem)))  # get rid of \n char
            time.sleep(0.2)  # lets not accidentally ddos their website


if __name__ == "__main__":
    # main()
    #get_website_from_code("LMS%3B%3B3%3BF")
    year, sem = "2023", "2"
    with open("test.txt", "w") as file:
        file.write("".join(func("LMS%3B%3B3%3BF", year, sem)))

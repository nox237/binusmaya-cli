import json
import requests
from binusmaya import URL
from termcolor import colored

def getSemesterList(session):
    # Getting the semester list
    print(f"[+] Getting semester in {URL}")
    headers = {"referer": "https://binusmaya.binus.ac.id/newStudent/"}
    response = session.post(URL + "services/ci/index.php/student/init/getStudentCourseMenuCourses", headers=headers)
    semester_list = json.loads(response.text)[0][3]
    print(colored(f"[+] Succesfully get semester list on {URL}", "green"))

    return semester_list

def setSemester(semester_list):
    temp = []
    print(colored("[!] Semester variable not set", "red"))
    print("[!] Listing semester from semester_list")
    for semester in semester_list:
        print(f"[!] Detecting {semester[1]}")
        temp.append(semester[1])
    print()

    print(f"[!] Choose Semester: ")
    for num, semester in enumerate(semester_list):
        print(f"[{num}] {semester[1]}")
    semester = int(input("[!] Input semester : "))
    print()

    return semester
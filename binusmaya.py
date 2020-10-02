#!/usr/bin/python3
import requests
import json
import re
import getopt
import sys
import stdiomask
import urllib.parse

from termcolor import colored
from bs4 import BeautifulSoup as bs

if sys.platform == "linux" or sys.platform == "linux2":
    # linux
    pass
elif sys.platform == "darwin":
    # MAC OS X
    pass
elif sys.platform == "win32" or sys.platform == "win64":
    # Windows 32-bit or Windows 64-bit
    import colorama
    colorama.init()


def login(session):
    global username_input
    try:
        print(f"[+] Connecting to {URL + 'login/'}")
        response = session.get(URL + "login/")
        if response.status_code:
            print(f"[+] Successfully connected to {URL + 'login/'}", end="\n\n")

            response_text = bs(response.text, "html.parser").find_all("input")
            username_name = response_text[0].get("name")
            password_name = response_text[1].get("name")
            submit_name = response_text[2].get("name")

            username_input = input("[!] Username Binusmaya (without @binus.ac.id) : ")
            password_input = stdiomask.getpass(mask='', prompt="[!] Password Binusmaya : ")
            print()

            if "@binusmaya.ac.id" in username_input:
                username_input = username_input.strip("@binusmaya.ac.id")

            real_username = input(f"[!] Enter your username (ENTER if your binusmaya mame is {' '.join(username_input.lower().split('.'))}): ")

            response_text = bs(response.text, "html.parser").find_all("script")
            loader_php = ""
            for response in response_text:
                try:
                    if "loader.php" in response.get("src"):
                        loader_php = response.get("src")
                        break
                except Exception as e:
                    continue

            print(f"[+] Getting CSRF token from {URL + loader_php[3:]}")
            response = session.get(URL + loader_php[3:])
            temp = re.findall(r"\$\(this\)\.append\(\'<input type=\"hidden\" name=\"([\w\d%]+)\" value=\"([\w\d%]+)\" \/>'\)\;", response.text)
            print(f"[+] Extracting CSRF token from {URL + loader_php[3:]}")
            csrf_one = temp[0]
            csrf_two = temp[1]

            print(f"[+] Sending POST request to {URL + 'login/'}")
            data = {username_name: username_input, password_name: password_input, submit_name: "login", csrf_one[0]: csrf_one[1], csrf_two[0]: csrf_two[1]}
            response = session.post(URL + "login/sys_login.php", data=data)
            if response.url == "https://binusmaya.binus.ac.id/newStudent/":
                print(colored(f"[+] Successfully login to {response.url}", "green"), end="\n\n")
            else:
                print(colored(f"[-] Failed login to {response.url}", "red"), end="\n\n")
                exit(1)

            if real_username != "":
                username_input = real_username
        else:
            print(colored(f"[-] {URL + 'login/'} not found", "red"))
            exit(1)
    except Exception as e:
        raise


def logout(session):
    global URL
    print(f"[+] Logging out from {URL}")
    temp_URL = URL + "services/ci/index.php/login/logout"
    session.get(temp_URL)

    temp_URL = URL + "simplesaml/module.php/core/as_logout.php?AuthId=default-sp&ReturnTo=https%3A%2F%2Fbinusmaya.binus.ac.id%2Flogin"
    session.get(temp_URL)
    print(f"[+] Successfully logging out from {URL}")


def getSemesterList(session):
    global semester_list

    # Getting the semester list
    print(f"[+] Getting semester in {URL}")
    headers = {"referer": "https://binusmaya.binus.ac.id/newStudent/"}
    response = s.post(URL + "services/ci/index.php/student/init/getStudentCourseMenuCourses", headers=headers)
    semester_list = json.loads(response.text)[0][3]
    print(colored(f"[+] Succesfully get semester list on {URL}", "green"))


def getAssignmentList(session):
    global URL, assignment_list, assignment_subject, assignment_complete

    for semester_subject in semester_list[semester][2:]:
        # Getting Attribute of the Semester_Subject
        CRSE_CODE = semester_subject['CRSE_CODE']
        CRSE_ID = semester_subject['CRSE_ID']
        STRM = semester_subject['STRM']
        SSR_COMPONENT = semester_subject['SSR_COMPONENT']
        CLASS_NBR = semester_subject['CLASS_NBR']

        # Getting the assignment list from the response
        headers = {"referer": "https://binusmaya.binus.ac.id/newStudent/"}
        response = s.get(f"https://binusmaya.binus.ac.id/services/ci/index.php/student/classes/assignmentType/{CRSE_CODE}/{CRSE_ID}/{STRM}/{SSR_COMPONENT}/{CLASS_NBR}/01", headers=headers)
        # https://binusmaya.binus.ac.id/services/ci/index.php/student/classes/basicinfo/010550/2010/LAB
        assignment_list_temp = json.loads(response.text)
        print(f"[+] Getting assignment on {semester_subject['COURSE_TITLE_LONG']}, ({semester_subject['SSR_COMPONENT']})")
        if assignment_list_temp != []:
            for assignment in assignment_list_temp:
                print(colored(f"[!] {assignment['Title']}", "yellow"))
                print(f" └─ Due date    : {assignment['deadlineTime']}, {assignment['deadlineDuration']}")

                data = {"id": str(assignment['StudentAssignmentID'])}
                response = s.post("https://binusmaya.binus.ac.id/services/ci/index.php/student/classes/getHistoryAssignment", json=data, headers=headers)
                submission_list = json.loads(response.text)
                for submission in submission_list:
                    print(colored(f"    [!] You already submit the answer on {submission['submittedDate']} ({submission['Title']})", "green"))
                    assignment_complete.append(assignment)
                if len(submission_list) == 0:
                    print(colored(f"    [-] Haven't submitted Yet", "red"))

            print()
            assignment_subject.append(semester_subject)
            assignment_list.append(assignment_list_temp)
        else:
            print(f"[-] There is no assignment on {semester_subject['COURSE_TITLE_LONG']}, ({semester_subject['SSR_COMPONENT']})")
    print()


def getForumList(session):
    global institution, acadCareer, period, courses, classes, topics, threads, replies

    print("[!] Starting scraping on forum")
    headers = {"referer": "https://binusmaya.binus.ac.id/newStudent/"}
    URL_getInstitution = "https://binusmaya.binus.ac.id/services/ci/index.php/forum/getInstitution"
    URL_getAcadCareer = "https://binusmaya.binus.ac.id/services/ci/index.php/forum/getAcadCareer"
    URL_getPeriod = "https://binusmaya.binus.ac.id/services/ci/index.php/forum/getPeriod"
    URL_getCourse = "https://binusmaya.binus.ac.id/services/ci/index.php/forum/getCourse"
    URL_getClass = "https://binusmaya.binus.ac.id/services/ci/index.php/forum/getClass"
    URL_getTopic = "https://binusmaya.binus.ac.id/services/ci/index.php/forum/getTopic"
    URL_getThread = "https://binusmaya.binus.ac.id/services/ci/index.php/forum/getThread"
    URL_getReply = "https://binusmaya.binus.ac.id/services/ci/index.php/forum/getReply"

    response = session.post(URL_getInstitution, headers=headers)
    getInstitution = json.loads(json.loads(response.text)['rows'])
    institution = getInstitution[0]
    print(f"[+] Set institution variable to {institution}")

    data = {"Institution": institution['ID']}
    response = session.post(URL_getAcadCareer, headers=headers, json=data)
    getAcadCareer = json.loads(json.loads(response.text)['rows'])
    acadCareer = getAcadCareer[0]
    print(f"[+] Set acadCareer variable to {acadCareer}")

    data = {"Institution": institution['ID'], 'acadCareer': acadCareer['ID']}
    response = session.post(URL_getPeriod, headers=headers, json=data)
    period = json.loads(json.loads(response.text)['rows'])
    print(f"[+] Set period variable to {period[semester]}")

    data = {"Institution": institution['ID'], 'acadCareer': acadCareer['ID'], 'period': period[semester]['ID']}
    response = session.post(URL_getCourse, headers=headers, json=data)
    courses_temp = json.loads(json.loads(response.text)['rows'])
    print("[+] Successfully getting all courses data", end="\n\n")

    for course in courses_temp:
        data = {"Institution": institution['ID'], 'acadCareer': acadCareer['ID'], 'period': period[semester]['ID'], 'course': course['ID']}
        response = session.post(URL_getClass, headers=headers, json=data)
        classes_temp = json.loads(json.loads(response.text)['rows'])
        print(f"[+] Successfully getting course data on {course['Caption']}")

        check_list_temp = []
        class_list_temp = []
        thread_list_temp = []
        topic_list_temp = []
        reply_list_temp = []
        status_thread = False

        for _class in classes_temp:
            data = {"Institution": institution['ID'], 'acadCareer': acadCareer['ID'], 'period': period[semester]['ID'], 'course': course['ID'], 'SESSIONIDNUM': ""}
            response = session.post(URL_getTopic, headers=headers, json=data)
            topics_temp = json.loads(json.loads(response.text)['rows'])
            print(f"[+] Successfully getting classes on {course['Caption']}")

            for topic in topics_temp:
                data = {"Institution": institution['ID'], 'acadCareer': acadCareer['ID'], 'period': period[semester]['ID'], 'course': course['ID'], 'SESSIONIDNUM': "", 'classid': _class['ID'], 'forumtypeid': 1, 'topic': topic['ID']}
                response = session.post(URL_getThread, headers=headers, json=data)
                threads_temp = json.loads(json.loads(response.text)['rows'])

                for thread in threads_temp:
                    if thread['ID'] != -1:
                        print(colored(f"[!] There is a thread on topic {topic['Caption']} : {urllib.parse.unquote(thread['ForumThreadTitle'])}, {thread['creator']}", "yellow"))
                        data = {"threadid": f"{thread['ID']}?id=1"}
                        response = session.post(URL_getReply, headers=headers, json=data)
                        replies_temp = json.loads(json.loads(response.text)['rows'])
                        status_answer = False
                        status_thread = True
                        class_list_temp.append(_class)
                        topic_list_temp.append(topic)
                        thread_list_temp.append(thread)
                        reply_list_temp.append(replies_temp)

                        for index, reply in enumerate(replies_temp):
                            if index == 0:
                                print(colored(f"[+] Lecturer Post: {urllib.parse.unquote(reply['PostContent'])}", "yellow"))

                            if ' '.join(username_input.lower().split('.')) in reply['Name'].lower() and status_answer == False:
                                print(colored(f"[+] You have answered the question: {reply['PostContent']}", 'green'))
                                status_answer = True
                                check_list_temp.append(True)

                        if status_answer == False:
                            print(colored(f"[!] You have not answered the question", 'red'))
                            check_list_temp.append(False)

                    else:
                        print(f"[!] There is no thread in {topic['Caption']}")
            print()

        if status_thread:
            courses.append(course)
            check_list.append(check_list_temp)
            classes.append(class_list_temp)
            topics.append(topic_list_temp)
            threads.append(thread_list_temp)
            replies.append(reply_list_temp)


def setSemester():
    global semester

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


def banner():
    print(" _____ _                               ")
    print("| __  |_|___ _ _ ___ _____ ___ _ _ ___ ")
    print("| __ -| |   | | |_ -|     | .'| | | .'|")
    print("|_____|_|_|_|___|___|_|_|_|__,|_  |__,|")
    print("                              |___|     by nox237", end="\n\n")


def help():
    print("COMMAND:")
    print(" -h, --help       : help command")
    print(' -s               : set semester to persistent index')
    print("ASSIGNMENT:")
    print(" -a, --assignment : scraping on the assignment")
    print(" -w               : write into assignment.md")
    print(" -o               : write into assignment_notion.md")
    print("FORUM:")
    print(" -f, --forum      : scraping on the forum")
    print(" -w               : write into forum.md  with lecturer post and user post")
    print(" -o               : write into forum_notion.md", end="\n\n")


def writeAssignmentToMarkdown():
    print("[!] Preparing writing assignment to a file")
    with open("assignment.md", "w") as f:
        f.write(f"# Assignment\n\n")
        for index, subject in enumerate(assignment_subject):
            f.write(f"## {subject['COURSE_TITLE_LONG']} ({subject['SSR_COMPONENT']})\n")
            for assignment in assignment_list[index]:
                if assignment in assignment_complete:
                    f.write(f"[x] {assignment['Title']}, deadline {assignment['deadlineTime']}, {assignment['deadlineDuration']}\n")
                else:
                    f.write(f"[ ] {assignment['Title']}, deadline {assignment['deadlineTime']}, {assignment['deadlineDuration']}\n")
                print(f"[+] Successfully writing {assignment['Title']}")
            f.write("\n")
    print(colored("[+] Successfully writing all assignment to assignment.md", "green"))
    print()


def writeForumToMarkdown():
    print("[!] Preparing writing forum to a file")
    with open("forum.md", "w") as f:
        f.write(f"# Forum\n\n")
        for index, course in enumerate(courses):
            f.write(f"## {course['Caption']}\n")
            for topic, thread, _class, check, reply in zip(topics[index], threads[index], classes[index], check_list[index], replies[index]):
                for index1, reply1 in enumerate(reply):
                    if index1 == 0:
                        if check:
                            f.write(f"[x] {topic['Caption']} ({_class['Caption']}), {urllib.parse.unquote(thread['ForumThreadTitle'])}\n")
                        else:
                            f.write(f"[ ] {topic['Caption']} ({_class['Caption']}), {urllib.parse.unquote(thread['ForumThreadTitle'])}\n")
                        f.write(f"    Lecturer Post: {urllib.parse.unquote(reply1['PostContent'])}\n")
                    if check:
                        if ' '.join(username_input.lower().split('.')) in reply1['Name'].lower():
                            f.write(f"    You have answered the question at {reply1['PostDate']} : {reply1['PostContent']}\n")
                            break
                print(f"[+] Successfully writing {topic['Caption']} {urllib.parse.unquote(thread['ForumThreadTitle'])}")
            f.write("\n")
    print(colored("[+] Successfully writing all thread to forum.md", "green"))
    print()


def writeAssignmentToMarkdownForNotion():
    print("[!] Preparing writing assignment to a file")
    with open("assignment_notion.md", "w") as f:
        f.write(f"# Assignment\n\n")
        for index, subject in enumerate(assignment_subject):
            f.write(f"## {subject['COURSE_TITLE_LONG']} ({subject['SSR_COMPONENT']})\n")
            for assignment in assignment_list[index]:
                if assignment in assignment_complete:
                    f.write(f"[x] {assignment['Title']}, deadline {assignment['deadlineTime']}, {assignment['deadlineDuration']}\n\n")
                else:
                    f.write(f"[ ] {assignment['Title']}, deadline {assignment['deadlineTime']}, {assignment['deadlineDuration']}\n\n")
                print(f"[+] Successfully writing {assignment['Title']}")
            f.write("\n")
    print(colored("[+] Successfully writing all assignment to assignment_notion.md", "green"))
    print()


def writeForumToMarkdownForNotion():
    print("[!] Preparing writing forum to a file")
    with open("forum_notion.md", "w") as f:
        f.write(f"# Forum\n\n")
        for index, course in enumerate(courses):
            f.write(f"## {course['Caption']}\n")
            for topic, thread, _class, check in zip(topics[index], threads[index], classes[index], check_list[index]):
                if check:
                    f.write(f"[x] {topic['Caption']} ({_class['Caption']}), {urllib.parse.unquote(thread['ForumThreadTitle'])}\n\n")
                else:
                    f.write(f"[ ] {topic['Caption']} ({_class['Caption']}), {urllib.parse.unquote(thread['ForumThreadTitle'])}\n\n")
                print(f"[+] Successfully writing {topic['Caption']} {urllib.parse.unquote(thread['ForumThreadTitle'])}")
            f.write("\n")
    print(colored("[+] Successfully writing all thread to forum_notion.md", "green"))
    print()


if __name__ == "__main__":
    s = requests.Session()
    opts, args = getopt.getopt(sys.argv[1:], "ohfaws:", ["help", "forum", "assignment"])

    banner()
    forum_listing = False
    assignment_listing = False

    URL = "https://binusmaya.binus.ac.id/"
    semester = -1
    semester_list = []
    username_input = ""
    real_username = ""

    check_list = []
    institution = []
    acadCareer = []
    period = []
    courses = []
    classes = []
    topics = []
    threads = []
    replies = []

    assignment_list = []
    assignment_subject = []
    assignment_complete = []

    status_refresh = False
    status_file_link = False
    status_write = False
    status_write_notion = False

    for opt, val in opts:
        if opt in ("-h", "--help"):
            help()
            exit(0)
        if opt in ("-w"):
            status_write = True
        if opt in ("-f", "--forum"):
            forum_listing = True
        if opt in ("-a", "--assignment"):
            assignment_listing = True
        if opt in ("-s"):
            semester = int(val)
        if opt in ("-o"):
            status_write_notion = True

    login(s)
    getSemesterList(s)
    if semester == -1:
        setSemester()
    else:
        print(f"[+] Set semester on {semester_list[semester][1]}")

    if forum_listing or assignment_listing:
        if assignment_listing:
            getAssignmentList(s)
            if status_write:
                writeAssignmentToMarkdown()
            if status_write_notion:
                writeAssignmentToMarkdownForNotion()
        if forum_listing:
            getForumList(s)
            if status_write:
                writeForumToMarkdown()
            if status_write_notion:
                writeForumToMarkdownForNotion()

    if forum_listing == False and assignment_listing == False:
        getAssignmentList(s)
        getForumList(s)
        writeAssignmentToMarkdown()
        writeForumToMarkdown()
        writeAssignmentToMarkdownForNotion()
        writeForumToMarkdownForNotion()

    logout(s)

import json
import requests
from binusmaya import URL
from termcolor import colored

def getAssignmentList(session, semester_list, semester):
    assignment_list = []
    assignment_subject = []
    assignment_complete = []

    print("[+] Getting all individual assignment in all courses")
    for semester_subject in semester_list[semester][2:]:
        # Getting Attribute of the Semester_Subject
        CRSE_CODE = semester_subject['CRSE_CODE']
        CRSE_ID = semester_subject['CRSE_ID']
        STRM = semester_subject['STRM']
        SSR_COMPONENT = semester_subject['SSR_COMPONENT']
        CLASS_NBR = semester_subject['CLASS_NBR']

        # Getting the assignment list from the response
        headers = {"referer": "https://binusmaya.binus.ac.id/newStudent/"}
        response = session.get(f"https://binusmaya.binus.ac.id/services/ci/index.php/student/classes/assignmentType/{CRSE_CODE}/{CRSE_ID}/{STRM}/{SSR_COMPONENT}/{CLASS_NBR}/01", headers=headers)
        # https://binusmaya.binus.ac.id/services/ci/index.php/student/classes/basicinfo/010550/2010/LAB

        assignment_list_temp = json.loads(response.text)
        print(f"[+] Getting assignment on {semester_subject['COURSE_TITLE_LONG']}, ({semester_subject['SSR_COMPONENT']})")
        if assignment_list_temp != []:
            for assignment in assignment_list_temp:
                print(colored(f"[!] {assignment['Title']}", "yellow"))
                print(f" └─ Due date    : {assignment['deadlineTime']}, {assignment['deadlineDuration']}")

                data = {"id": str(assignment['StudentAssignmentID'])}
                response = session.post("https://binusmaya.binus.ac.id/services/ci/index.php/student/classes/getHistoryAssignment", json=data, headers=headers)
                submission_list = json.loads(response.text)
                for submission in submission_list:
                    print(colored(f"    [!] You already submit the answer on {submission['submittedDate']} ({submission['Title']})", "green"))
                    assignment_complete.append(assignment)
                if len(submission_list) == 0:
                    print(colored(f"    [-] Haven't submitted Yet", "red"))
            assignment_subject.append(semester_subject)
            assignment_list.append(assignment_list_temp)
        else:
            print(f"[-] There is no assignment on {semester_subject['COURSE_TITLE_LONG']}, ({semester_subject['SSR_COMPONENT']})")
    print()
    print("[+] Getting all group assignment in all courses")
    for semester_subject in semester_list[semester][2:]:
        # Getting Attribute of the Semester_Subject
        CRSE_CODE = semester_subject['CRSE_CODE']
        CRSE_ID = semester_subject['CRSE_ID']
        STRM = semester_subject['STRM']
        SSR_COMPONENT = semester_subject['SSR_COMPONENT']
        CLASS_NBR = semester_subject['CLASS_NBR']

        # Getting the assignment list from the response
        headers = {"referer": "https://binusmaya.binus.ac.id/newStudent/"}
        response = session.get(f"https://binusmaya.binus.ac.id/services/ci/index.php/student/classes/assignmentType/{CRSE_CODE}/{CRSE_ID}/{STRM}/{SSR_COMPONENT}/{CLASS_NBR}/02", headers=headers)
        # https://binusmaya.binus.ac.id/services/ci/index.php/student/classes/basicinfo/010550/2010/LAB

        assignment_list_temp = json.loads(response.text)
        print(f"[+] Getting assignment on {semester_subject['COURSE_TITLE_LONG']}, ({semester_subject['SSR_COMPONENT']})")
        if assignment_list_temp != []:
            for assignment in assignment_list_temp:
                print(colored(f"[!] {assignment['Title']}", "yellow"))
                print(f" └─ Due date    : {assignment['deadlineTime']}, {assignment['deadlineDuration']}")

                data = {"id": str(assignment['StudentAssignmentID'])}
                response = session.post("https://binusmaya.binus.ac.id/services/ci/index.php/student/classes/getHistoryAssignment", json=data, headers=headers)
                submission_list = json.loads(response.text)
                for submission in submission_list:
                    print(colored(f"    [!] You already submit the answer on {submission['submittedDate']} ({submission['Title']})", "green"))
                    assignment_complete.append(assignment)
                if len(submission_list) == 0:
                    print(colored(f"    [-] Haven't submitted Yet", "red"))
            assignment_subject.append(semester_subject)
            assignment_list.append(assignment_list_temp)
        else:
            print(f"[-] There is no assignment on {semester_subject['COURSE_TITLE_LONG']}, ({semester_subject['SSR_COMPONENT']})")
    print()

    return assignment_list, assignment_subject, assignment_complete


def writeAssignmentToMarkdown(storage_path, assignment_list, assignment_subject, assignment_complete):
    print("[!] Preparing writing assignment to a file")
    with open(storage_path + "assignment.md", "w") as f:
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


def writeAssignmentToMarkdownForNotion(storage_path, assignment_list, assignment_subject, assignment_complete):
    print("[!] Preparing writing assignment to a file")
    with open(storage_path + "assignment_notion.md", "w") as f:
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
#!/usr/bin/python3
import os
import sys
import getopt
import requests
from termcolor import colored
from binusmaya import auth, assignment, enrichment, forum, todolist, utility


STORAGE_LOCATION = os.path.dirname(__file__) + '/storage/'
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


def banner():
    print(" _____ _                               ")
    print("| __  |_|___ _ _ ___ _____ ___ _ _ ___ ")
    print("| __ -| |   | | |_ -|     | .'| | | .'|")
    print("|_____|_|_|_|___|___|_|_|_|__,|_  |__,|")
    print("                              |___|     by nox237", end="\n\n")


def help():
    print("COMMAND:")
    print(" --all            : run all available command")
    print(" -h, --help       : help command")
    print(' -s               : set semester to persistent index')
    print("ASSIGNMENT:")
    print(" -a, --assignment : scraping on the assignment")
    print(" -w               : write into assignment.md")
    print(" -o               : write into assignment_notion.md")
    print("FORUM:")
    print(" -f, --forum      : scraping on the forum")
    print(" -w               : write into forum.md  with lecturer post and user post")
    print(" -o               : write into forum_notion.md")
    print("TODOLIST:")
    print(" -t, --todolist   : scraping on the todolist")
    print(" -w               : write into todolist.md")
    print("ENRICHMENT:")
    print(" --enrichment     : scraping enrichment page")
    print(" -e               : set enrichment semester (do not need --enrichment flag)")
    print(" -m               : for mobile view", end="\n\n")
    print(" --progressbar    : print progressbar for each thread request")
    print(" --detailwrite    : output detail write on forum.md", end="\n\n")


if __name__ == "__main__":
    s = requests.Session()
    opts, args = getopt.getopt(sys.argv[1:], "ohfamwts:e:", ["help", "forum", "assignment", "todolist", "enrichment", "progressbar", "all"])

    banner()
    forum_listing = False
    assignment_listing = False

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

    todo_list = []

    status_refresh = False
    status_file_link = False
    status_write = False
    status_write_notion = False
    status_progressbar = False
    status_detail_write = False
    todo_list_status = False

    scan_all = False

    enrichment_semester = -1
    enrichment_status = False
    enrichment_mobile_view = False

    for opt, val in opts:
        if opt in ("-h", "--help"):
            help()
            exit(0)
        if opt in ("-m"):
            enrichment_mobile_view = True
        if opt in ("-w"):
            status_write = True
        if opt in ("-f", "--forum"):
            forum_listing = True
        if opt in ("-a", "--assignment"):
            assignment_listing = True
        if opt in ("-s"):
            semester = int(val)
        if opt in ("-t", "--todolist"):
            todo_list_status = True
        if opt in ("-e"):
            enrichment_status = True
            enrichment_semester = int(val)
        if opt in ("--enrichment"):
            enrichment_status = True
        if opt in ("-o"):
            status_write_notion = True
        if opt in ("--progressbar"):
            status_progressbar = True
        if opt in ("--detailwrite"):
            status_detail_write = True
        if opt in ("--all"):
            scan_all = True

    if not os.path.exists(STORAGE_LOCATION):
        print('[!] There is no storage directory')
        os.mkdir(STORAGE_LOCATION)
        print(colored('[+] Create storage directory', 'green'), end="\n\n")

    auth.login(s)

    if forum_listing or assignment_listing or todo_list_status:
        semester_list = utility.getSemesterList(s)
        if semester == -1:
            semester = utility.setSemester(semester_list)
        else:
            print(f"[+] Set semester on {semester_list[semester][1]}")

        if assignment_listing:
            assignment_list, assignment_subject, assignment_complete = assignment.getAssignmentList(s, semester_list, semester)
            if status_write:
                assignment.writeAssignmentToMarkdown(STORAGE_LOCATION, assignment_list, assignment_subject, assignment_complete)
            if status_write_notion:
                assignment.writeAssignmentToMarkdownForNotion(STORAGE_LOCATION, assignment_list, assignment_subject, assignment_complete)
        if forum_listing:
            institution, acadCareer, period, courses, classes, topics, threads, replies, check_list = forum.getForumList(s, institution, acadCareer, period, courses, classes, topics, threads, replies, check_list, semester)
            if status_write:
                forum.writeForumToMarkdown(STORAGE_LOCATION, check_list, courses, classes, topics, threads, replies)
            if status_write_notion:
                forum.writeForumToMarkdownForNotion(STORAGE_LOCATION, check_list, courses, classes, topics, threads, replies)
        if todo_list_status:
            todo_list = todolist.getToDoList(s, todo_list)
            todolist.printToDoList(todo_list)

    if scan_all:
        semester_list = utility.getSemesterList(s)
        if semester == -1:
            semester = utility.setSemester(semester_list)
        else:
            print(f"[+] Set semester on {semester_list[semester][1]}")
            
        assignment_list, assignment_subject, assignment_complete = assignment.getAssignmentList(s, semester_list, semester)
        institution, acadCareer, period, courses, classes, topics, threads, replies, check_list = forum.getForumList(s, institution, acadCareer, period, courses, classes, topics, threads, replies, check_list, semester)
        todo_list = todolist.getToDoList(s, todo_list)

        assignment.writeAssignmentToMarkdown(STORAGE_LOCATION, assignment_list, assignment_subject, assignment_complete)
        forum.writeForumToMarkdown(STORAGE_LOCATION, check_list, courses, classes, topics, threads, replies)
        assignment.writeAssignmentToMarkdownForNotion(STORAGE_LOCATION, assignment_list, assignment_subject, assignment_complete)
        forum.writeForumToMarkdownForNotion(STORAGE_LOCATION, check_list, courses, classes, topics, threads, replies)
        todolist.printToDoList(todo_list)

    if enrichment_status:
        temp_response = enrichment.login_to_enrichment(s)
        strm = enrichment.get_semester_enrichment(s, enrichment_semester, temp_response)
        enrichment.get_enrichment_information(s, enrichment_semester, strm, enrichment_mobile_view)

    auth.logout(s)

if sys.platform == "linux" or sys.platform == "linux2":
    # linux
    pass
elif sys.platform == "darwin":
    # MAC OS X
    pass
elif sys.platform == "win32" or sys.platform == "win64":
    # Windows 32-bit or Windows 64-bit
    input("[!] Press ENTER to exit ...")

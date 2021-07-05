import json
import requests
from termcolor import colored
from binusmaya import URL


def printToDoList(todo_list):
    if len(todo_list) > 0:
        print(colored(f"[!] There is {len(todo_list)} todo list", "yellow"))
        for todo in todo_list:
            print(colored(f"\n[!] {todo['Title']}", "yellow"))
            print(f" |─ Description         : {todo['Description']}")
            print(f" |─ Mandatory Status    : {todo['MandatoryStatus']}")
            print(f" |─ Activity Status     : {todo['ActivityStatus']}")
            print(f" |─ Location            : {todo['Location']}")
            print(f" └─ Due date            : {todo['DueDate']}, {todo['Time']}")
    else:
        print(colored("[!] There is no todo list", "green"))
    print()


def getToDoList(session, todo_list):

    # Getting the todo list
    print(f"[+] Getting todo list in {URL}")
    headers = {"referer": "https://binusmaya.binus.ac.id/newStudent/"}
    response = session.post(
        URL + "services/ci/index.php/student/general/todo/list", headers=headers
    )
    todo_list = json.loads(response.text)
    print(colored(f"[+] Succesfully get todo list on {URL}", "green"))
    return todo_list

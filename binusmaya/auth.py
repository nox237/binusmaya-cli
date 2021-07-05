import re
import requests
import stdiomask
from binusmaya import URL
from termcolor import colored
from bs4 import BeautifulSoup as bs

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
            if "error" not in response.url:
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
    print(f"[+] Logging out from {URL}")
    temp_URL = URL + "services/ci/index.php/login/logout"
    session.get(temp_URL)

    temp_URL = URL + "simplesaml/module.php/core/as_logout.php?AuthId=default-sp&ReturnTo=https%3A%2F%2Fbinusmaya.binus.ac.id%2Flogin"
    session.get(temp_URL)
    print(f"[+] Successfully logging out from {URL}")
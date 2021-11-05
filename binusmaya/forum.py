import json
import requests
import urllib
from binusmaya import URL
from termcolor import colored


def getForumList(
    session,
    institution,
    acadCareer,
    period,
    courses,
    classes,
    topics,
    threads,
    replies,
    check_list,
    semester,
    status_progressbar,
    username_input,
):
    print("[!] Starting scraping on forum")
    headers = {"referer": "https://binusmaya.binus.ac.id/newStudent/"}
    URL_getInstitution = (
        "https://binusmaya.binus.ac.id/services/ci/index.php/forum/getInstitution"
    )
    URL_getAcadCareer = (
        "https://binusmaya.binus.ac.id/services/ci/index.php/forum/getAcadCareer"
    )
    URL_getPeriod = (
        "https://binusmaya.binus.ac.id/services/ci/index.php/forum/getPeriod"
    )
    URL_getCourse = (
        "https://binusmaya.binus.ac.id/services/ci/index.php/forum/getCourse"
    )
    URL_getClass = "https://binusmaya.binus.ac.id/services/ci/index.php/forum/getClass"
    URL_getTopic = "https://binusmaya.binus.ac.id/services/ci/index.php/forum/getTopic"
    URL_getThread = (
        "https://binusmaya.binus.ac.id/services/ci/index.php/forum/getThread"
    )
    URL_getReply = "https://binusmaya.binus.ac.id/services/ci/index.php/forum/getReply"

    response = session.post(URL_getInstitution, headers=headers)
    getInstitution = json.loads(json.loads(response.text)["rows"])
    institution = getInstitution[0]
    print(f"[+] Set institution variable to {institution}")

    data = {"Institution": institution["ID"]}
    response = session.post(URL_getAcadCareer, headers=headers, json=data)
    getAcadCareer = json.loads(json.loads(response.text)["rows"])
    acadCareer = getAcadCareer[0]
    print(f"[+] Set acadCareer variable to {acadCareer}")

    data = {"Institution": institution["ID"], "acadCareer": acadCareer["ID"]}
    response = session.post(URL_getPeriod, headers=headers, json=data)
    period = json.loads(json.loads(response.text)["rows"])
    print(f"[+] Set period variable to {period[semester]}")

    data = {
        "Institution": institution["ID"],
        "acadCareer": acadCareer["ID"],
        "period": period[semester]["ID"],
    }
    response = session.post(URL_getCourse, headers=headers, json=data)
    courses_temp = json.loads(json.loads(response.text)["rows"])
    print("[+] Successfully getting all courses data", end="\n\n")

    for course in courses_temp:
        data = {
            "Institution": institution["ID"],
            "acadCareer": acadCareer["ID"],
            "period": period[semester]["ID"],
            "course": course["ID"],
        }
        response = session.post(URL_getClass, headers=headers, json=data)
        classes_temp = json.loads(json.loads(response.text)["rows"])
        print(f"[+] Successfully getting course data on {course['Caption']}")

        check_list_temp = []
        class_list_temp = []
        thread_list_temp = []
        topic_list_temp = []
        reply_list_temp = []
        status_thread = False

        for _class in classes_temp:
            data = {
                "Institution": institution["ID"],
                "acadCareer": acadCareer["ID"],
                "period": period[semester]["ID"],
                "course": course["ID"],
                "SESSIONIDNUM": "",
            }
            response = session.post(URL_getTopic, headers=headers, json=data)
            topics_temp = json.loads(json.loads(response.text)["rows"])
            print(f"[+] Successfully getting classes on {course['Caption']}")

            for topic in topics_temp:
                data = {
                    "Institution": institution["ID"],
                    "acadCareer": acadCareer["ID"],
                    "period": period[semester]["ID"],
                    "course": course["ID"],
                    "SESSIONIDNUM": "",
                    "classid": _class["ID"],
                    "forumtypeid": 1,
                    "topic": topic["ID"],
                }
                response = session.post(
                    URL_getThread, headers=headers, json=data)
                threads_temp = json.loads(json.loads(response.text)["rows"])

                for thread in threads_temp:
                    if thread["ID"] != -1:
                        print(
                            colored(
                                f"[!] There is a thread on topic {topic['Caption']} : {urllib.parse.unquote(thread['ForumThreadTitle'])}, {thread['creator']}",
                                "yellow",
                            )
                        )
                        data = {"threadid": f"{thread['ID']}?id=1"}

                        if status_progressbar:
                            response = session.post(
                                URL_getReply, headers=headers, json=data, stream=True
                            )
                            json_data = ""
                            total_size = int(
                                response.headers["Content-Length"])
                            for response_data in tqdm(
                                iterable=response.iter_content(
                                    chunk_size=1024),
                                total=int(total_size / 1024),
                                unit="KB",
                                leave=False,
                            ):
                                json_data += response_data.decode()
                            replies_temp = json.loads(
                                json.loads(json_data)["rows"])
                        else:
                            response = session.post(
                                URL_getReply, headers=headers, json=data
                            )
                            replies_temp = json.loads(
                                json.loads(response.text)["rows"])

                        status_answer = False
                        status_thread = True
                        class_list_temp.append(_class)
                        topic_list_temp.append(topic)
                        thread_list_temp.append(thread)
                        reply_list_temp.append(replies_temp)

                        for index, reply in enumerate(replies_temp):
                            if index == 0:
                                print(
                                    colored(
                                        f"[+] Lecturer Post: {urllib.parse.unquote(reply['PostContent'])}",
                                        "yellow",
                                    )
                                )

                            if (
                                " ".join(username_input.lower().split("."))
                                in reply["Name"].lower()
                                and status_answer == False
                            ):
                                print(
                                    colored(
                                        f"[+] You have answered the question: {reply['PostContent']}",
                                        "green",
                                    )
                                )
                                status_answer = True
                                check_list_temp.append(True)

                        if status_answer == False:
                            print(
                                colored(
                                    f"[!] You have not answered the question", "red"
                                )
                            )
                            check_list_temp.append(False)

                    else:
                        print(f"[!] There is no thread in {topic['Caption']}")

            data = {
                "Institution": institution["ID"],
                "acadCareer": acadCareer["ID"],
                "period": period[semester]["ID"],
                "course": course["ID"],
                "SESSIONIDNUM": "",
                "classid": _class["ID"],
                "forumtypeid": 1,
                "topic": "",
            }
            response = session.post(URL_getThread, headers=headers, json=data)
            threads_temp = json.loads(json.loads(response.text)["rows"])

            if len(threads_temp) > 0:
                ANSWERED_STATUS = False
                print(colored("[+] There is a thread in All/other", "green"))
                for thread in threads_temp:
                    if thread["ID"] != -1:
                        if thread not in thread_list_temp:
                            print(
                                colored(
                                    f"[!] There is a thread on topic {topic['Caption']} : {urllib.parse.unquote(thread['ForumThreadTitle'])}, {thread['creator']}",
                                    "yellow",
                                )
                            )
                            data = {"threadid": f"{thread['ID']}?id=1"}

                            if status_progressbar:
                                response = session.post(
                                    URL_getReply,
                                    headers=headers,
                                    json=data,
                                    stream=True,
                                )
                                json_data = ""
                                total_size = int(
                                    response.headers["Content-Length"])
                                for response_data in tqdm(
                                    iterable=response.iter_content(
                                        chunk_size=1024),
                                    total=int(total_size / 1024),
                                    unit="KB",
                                    leave=False,
                                ):
                                    json_data += response_data.decode()
                                replies_temp = json.loads(
                                    json.loads(json_data)["rows"])
                            else:
                                response = session.post(
                                    URL_getReply, headers=headers, json=data
                                )
                                replies_temp = json.loads(
                                    json.loads(response.text)["rows"]
                                )

                            status_answer = False
                            status_thread = True
                            class_list_temp.append(_class)
                            topic_list_temp.append(topic)
                            thread_list_temp.append(thread)
                            reply_list_temp.append(replies_temp)

                            for index, reply in enumerate(replies_temp):
                                if index == 0:
                                    print(
                                        colored(
                                            f"[+] Lecturer Post: {urllib.parse.unquote(reply['PostContent'])}",
                                            "yellow",
                                        )
                                    )

                                if (
                                    " ".join(username_input.lower().split("."))
                                    in reply["Name"].lower()
                                    and status_answer == False
                                ):
                                    print(
                                        colored(
                                            f"[+] You have answered the question: {reply['PostContent']}",
                                            "green",
                                        )
                                    )
                                    status_answer = True
                                    check_list_temp.append(True)
                            if status_answer == False:
                                print(
                                    colored(
                                        f"[!] You have not answered the question", "red"
                                    )
                                )
                                check_list_temp.append(False)
                            ANSWERED_STATUS = True
                if ANSWERED_STATUS == False:
                    print(
                        colored(
                            "[+] All thread in All/other is the same as above", "green"
                        )
                    )
            else:
                print(colored("[+] There is no thread in All/other", "green"))
            print()

        if status_thread:
            courses.append(course)
            check_list.append(check_list_temp)
            classes.append(class_list_temp)
            topics.append(topic_list_temp)
            threads.append(thread_list_temp)
            replies.append(reply_list_temp)

    return (
        institution,
        acadCareer,
        period,
        courses,
        classes,
        topics,
        threads,
        replies,
        check_list,
    )


def writeForumToMarkdown(
    storage_path, check_list, courses, classes, topics, threads, replies, status_detail_write
):
    print("[!] Preparing writing forum to a file")
    with open(storage_path + "forum.md", "w") as f:
        f.write(f"# Forum\n\n")
        for index, course in enumerate(courses):
            f.write(f"## {course['Caption']}\n")
            for topic, thread, _class, check, reply in zip(
                topics[index],
                threads[index],
                classes[index],
                check_list[index],
                replies[index],
            ):
                for index1, reply1 in enumerate(reply):
                    if index1 == 0:
                        if check:
                            f.write(
                                f"[x] {topic['Caption']} ({_class['Caption']}), {urllib.parse.unquote(thread['ForumThreadTitle'])}\n"
                            )
                        else:
                            f.write(
                                f"[ ] {topic['Caption']} ({_class['Caption']}), {urllib.parse.unquote(thread['ForumThreadTitle'])}\n"
                            )
                        if status_detail_write:
                            f.write(
                                f"    Lecturer Post: {urllib.parse.unquote(reply1['PostContent'])}\n"
                            )
                    if check and status_detail_write:
                        if (
                            " ".join(username_input.lower().split("."))
                            in reply1["Name"].lower()
                        ):
                            f.write(
                                f"    You have answered the question at {reply1['PostDate']} : {reply1['PostContent']}\n"
                            )
                            break
                print(
                    f"[+] Successfully writing {topic['Caption']} {urllib.parse.unquote(thread['ForumThreadTitle'])}"
                )
            f.write("\n")
    print(colored("[+] Successfully writing all thread to forum.md", "green"))
    print()


def writeForumToMarkdownForNotion(
    storage_path, check_list, courses, classes, topics, threads, replies
):
    print("[!] Preparing writing forum to a file")
    with open(storage_path + "forum_notion.md", "w") as f:
        f.write(f"# Forum\n\n")
        for index, course in enumerate(courses):
            f.write(f"## {course['Caption']}\n")
            for topic, thread, _class, check in zip(
                topics[index], threads[index], classes[index], check_list[index]
            ):
                if check:
                    f.write(
                        f"[x] {topic['Caption']} ({_class['Caption']}), {urllib.parse.unquote(thread['ForumThreadTitle'])}\n\n"
                    )
                else:
                    f.write(
                        f"[ ] {topic['Caption']} ({_class['Caption']}), {urllib.parse.unquote(thread['ForumThreadTitle'])}\n\n"
                    )
                print(
                    f"[+] Successfully writing {topic['Caption']} {urllib.parse.unquote(thread['ForumThreadTitle'])}"
                )
            f.write("\n")
    print(
        colored("[+] Successfully writing all thread to forum_notion.md", "green"))
    print()

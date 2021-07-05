#!/usr/bin/python3
import json
import requests

from termcolor import colored
from bs4 import BeautifulSoup as bs
from prettytable import PrettyTable
from binusmaya import auth


class Intern:
    """Internship Model"""

    def __init__(
        self,
        address,
        available,
        attachmentPath,
        city,
        companyName,
        desc,
        district,
        duration,
        startDate,
        endDate,
        isMinimalGPA,
        position,
        province,
        quota,
        subdistrict,
        workStatus,
        zipCode,
        partnerDTO,
    ):
        (
            self.address,
            self.available,
            self.attachmentPath,
            self.city,
            self.companyName,
            self.desc,
            self.district,
            self.duration,
            self.startDate,
            self.endDate,
            self.isMinimalGPA,
            self.position,
            self.province,
            self.quota,
            self.subdistrict,
            self.workStatus,
            self.zipCode,
            self.partnerDTO,
        ) = (
            address,
            available,
            attachmentPath,
            city,
            companyName,
            desc,
            district,
            duration,
            startDate,
            endDate,
            isMinimalGPA,
            position,
            province,
            quota,
            subdistrict,
            workStatus,
            zipCode,
            partnerDTO,
        )


class Intern_apply:
    """Applied Intern Model"""

    def __init__(
        self, Company, Position, Duration, Start_Date, End_Date, Status, Notes
    ):
        (
            self.company,
            self.position,
            self.duration,
            self.startDate,
            self.endDate,
            self.status,
            self.note,
        ) = (Company, Position, Duration, Start_Date, End_Date, Status, Notes)


URL = "https://binusmaya.binus.ac.id/"
BASE_URL_ENRICHMENT = "https://enrichment.apps.binus.ac.id/"
BASE_URL_INTERNSHIP = "https://internship.apps.binus.ac.id/"


def login_to_enrichment(session):
    headers = {"referer": "https://binusmaya.binus.ac.id/newStudent/"}
    print(colored(f"[!] Trying to get access into {BASE_URL_ENRICHMENT}", "yellow"))
    print(
        f'[+] Getting the token from {URL + "services/ci/index.php/student/enrichmentApps/GetToken/"}'
    )
    token = session.get(
        URL + "services/ci/index.php/student/enrichmentApps/GetToken/", headers=headers
    )
    print(
        f'[+] Getting the SSO token from {URL + "services/ci/index.php/student/enrichmentApps/GenerateSSOTokenEnrichment/"} for Enrichment Apps'
    )
    data = {"Token": token.text[1:-1]}
    sso_token = session.post(
        URL
        + "services/ci/index.php/student/enrichmentApps/GenerateSSOTokenEnrichment/",
        json=data,
        headers=headers,
    )
    response = session.get(
        BASE_URL_ENRICHMENT +
        "Login/Student/SSO?t={}".format(sso_token.text[1:-1])
    )
    print(colored("[!] Successfully login to Enrichment Apps",
                  "green"), end="\n\n")
    return response


def get_semester_enrichment(session, semester, response):
    print("[+] Getting all the semester from Enrichment Apps")
    options = bs(response.text, "html.parser").find(
        "select").find_all("option")

    if semester == -1:
        print("[!] Choose semester:")
        while True:
            for i, value in enumerate(options):
                print(f"[{i}] {value.getText()}")
            semester = int(input(">>> "))
            if semester >= 0 and semester <= len(options) - 1:
                break
            else:
                print("[!] Invalid semester number")
    print(colored(f"[!] Using semester {options[semester].getText()}", "yellow"))
    strm = options[semester].get("value")
    return strm


def get_internship_information(s, semester, strm, mobile_view, response):
    print(f"[+] Redirecting to {BASE_URL_INTERNSHIP}")
    link_to_enrichment = (
        bs(response, "html.parser")
        .find("a", {"class": "button-orange"})
        .get("href")[1:]
    )
    response_2 = s.get(BASE_URL_ENRICHMENT + link_to_enrichment)

    data = {
        "draw": "1",
        "start": "0",
        "length": "10",
        "columns[0][data]": "",
        "columns[0][name]": "",
        "columns[0][searchable]": "true",
        "columns[0][orderable]": "true",
        "columns[0][search][value]": "",
        "columns[0][search][regex]": "false",
        "columns[1][data]": "",
        "columns[1][name]": "",
        "columns[1][searchable]": "true",
        "columns[1][orderable]": "true",
        "columns[1][search][value]": "",
        "columns[1][search][regex]": "false",
        "columns[2][data]": "",
        "columns[2][name]": "",
        "columns[2][searchable]": "true",
        "columns[2][orderable]": "true",
        "columns[2][search][value]": "",
        "columns[2][search][regex]": "false",
        "search[value]": "",
        "search[regex]": "false",
        "order[0][column]": "0",
        "order[0][dir]": "asc",
    }
    headers = {"referer": "https://internship.apps.binus.ac.id/Dashboard/Student"}
    response_3 = s.post(
        BASE_URL_INTERNSHIP + "Jobs/Student/StudentJobTable", headers=headers, data=data
    )
    internship_offering = json.loads(response_3.text)

    response = s.get(BASE_URL_INTERNSHIP +
                     "Dashboard/Student", headers=headers)
    table = bs(response.text, "html.parser").find("table").find_all("tr")
    intern_status = []
    x = PrettyTable()
    print(colored("[!] Getting all applied internship", "yellow"))
    if mobile_view:
        print("[!] Setting up on the mobile view")
        x.field_names = ["Company", "Position",
                         "Start Date", "End Date", "Status"]
        x._max_width = {"Company": 30, "Position": 45, "Status": 15}
    else:
        print("[!] Setting up on the desktop view")
        x.field_names = [
            "Company",
            "Position",
            "Duration",
            "Start Date",
            "End Date",
            "Status",
            "Notes",
        ]
        x._max_width = {"Company": 30, "Position": 45, "Status": 15}
    for table_row in table:
        temp_table_column = table_row.find_all("th")
        if temp_table_column == []:
            temp_array = []
            for table_column in table_row.find_all("td"):
                temp_array.append(table_column.getText().strip())
            if mobile_view:
                x.add_row(
                    [
                        temp_array[0],
                        temp_array[1],
                        temp_array[3],
                        temp_array[4],
                        temp_array[5],
                    ]
                )
            else:
                x.add_row(
                    [
                        temp_array[0],
                        temp_array[1],
                        temp_array[2],
                        temp_array[3],
                        temp_array[4],
                        temp_array[5],
                        temp_array[6],
                    ]
                )
    print(x, end="\n\n")

    x = PrettyTable()
    if mobile_view:
        print("[!] Setting up on the mobile view")
        x.field_names = ["Position", "Company", "JobAvailable"]
        x._max_width = {"Position": 30, "Company": 45, "JobAvailable": 15}
    else:
        print("[!] Setting up on the desktop view")
        x.field_names = [
            "Position",
            "Company",
            "City",
            "Address",
            "JobAvailable",
            "StartDate",
            "EndDate",
            "WorkStatus",
        ]
        x._max_width = {
            "Position": 30,
            "Company": 45,
            "JobAvailable": 15,
            "Address": 50,
        }
    print(
        colored(
            f"[!] Total position available : {internship_offering['recordsTotal']}",
            "yellow",
        )
    )

    for internship in internship_offering["data"]:
        # For Debugging
        # print(json.dumps(internship_offering,sort_keys=True, indent=4))
        # exit(0)

        # Each data contains:
        # address, attachmentPath, available, categoryId, city, companyName, desc, district, duration, emplid, endDate, hasrenew, isMinimalGPA, isViewed, jobAvailable, jobId, jobTypeDesc,
        # jobTypeId, locationId, minimumJob, partnerDTO, partnerId, partnerImagePath, position, province, quota, startDate, status, statusName, strm, subdistrict, workStatus, workStatusId, zipCode

        # partnerDTO contains:
        # dateIn, dateUp, partnerAddress, partnerCity, partnerDesc, partnerDistrict, partnerEmail, partnerId, partnerImagePath, partnerPICEmail, partnerPICEmail, partnerPICName, partnerPICPhone,
        # partnerPhone, partnerProvince, partnerSubdistrict, partnerType, partnerTypeId, partnerWebsite, partnerZipCode, statusId, strSc, userIn, userUp

        internship = Intern(
            internship["address"],
            internship["available"],
            internship["attachmentPath"],
            internship["city"],
            internship["companyName"],
            internship["desc"],
            internship["district"],
            internship["duration"],
            internship["startDate"],
            internship["endDate"],
            internship["isMinimalGPA"],
            internship["position"],
            internship["province"],
            internship["quota"],
            internship["subdistrict"],
            internship["workStatus"],
            internship["zipCode"],
            internship["partnerDTO"],
        )
        if mobile_view:
            x.add_row(
                [
                    internship.position,
                    internship.companyName,
                    f"{internship.available}/{internship.quota}",
                ]
            )
        else:
            x.add_row(
                [
                    internship.position,
                    internship.companyName,
                    internship.city,
                    internship.address,
                    f"{internship.available}/{internship.quota}",
                    internship.startDate,
                    internship.endDate,
                    internship.workStatus,
                ]
            )

    print(x, end="\n\n")


def get_enrichment_information(s, semester, strm, mobile_view):
    data = {"Strm": strm}
    headers = {"referer": "https://enrichment.apps.binus.ac.id/"}
    response = s.post(
        BASE_URL_ENRICHMENT + "Dashboard/Student/IndexStudentDashboard",
        data=data,
        headers=headers,
    )
    print()

    if "Go to Internship Apps" in response.text:
        get_internship_information(
            s, semester, strm, mobile_view, response.text)

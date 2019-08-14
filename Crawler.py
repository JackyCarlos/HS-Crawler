#!/usr/bin/env python3

import requests
import getpass
import re
import os
import Tools

fileExtensions = ('.pdf', '.docx', '.txt')
loginPage = 'https://elearning.hs-offenburg.de/moodle/login/index.php'
ignoredCourses = []
tastyCookie = {}


def setupLogin():
    print('This tool logs into the moodle account you specify and downloads all the files within the courses and saves'
          ' them to a folder of your choice.')

    username = input('please provide username for your moodle-account: ')
    password = getpass.getpass('please provide password for your moodle-account: ')
    saveLocation = input('please specify a location in your home directory starting with \'~/\': ')

    return username, password, saveLocation


def moodleLogin(username, password):
    session = requests.session()

    try:
        hsPage = session.get(loginPage).text

        # in order to login we have to submit a token. Every time we enter the page to login a new one gets generated.
        loginToken = re.findall(r'name="logintoken" value="([a-zA-Z0-9]*)"', hsPage)

        loginCredentials = {'username': username, 'password': password, 'logintoken': loginToken[0]}

        siteLogin = session.post(loginPage, data=loginCredentials).text
        tastyCookie.update(session.cookies.get_dict())

    except Exception:
        print('The moodle site appears to be down. Check your internet connection. ')
        exit(0)

    # check for a failed login atempt
    if failedLogin(siteLogin):
        print('invalid login credentials')

        exit(0)

    session.close()

    return siteLogin


def crawlCourses(moodleStartPage):
    courses = Tools.removeDuplicates(re.findall(r'course/view\.php\?id=([0-9]{4,})"', moodleStartPage))

    for course in courses:
        if course not in ignoredCourses:
            downloadCourseFiles('https://elearning.hs-offenburg.de/moodle/course/view.php?id=' + str(course))


def downloadCourseFiles(url):
    session = requests.session()

    coursePage = session.get(url, cookies=tastyCookie).text

    documentsID = re.findall(r'/mod/resource/view\.php\?id=([0-9]*)', coursePage)

    for fileID in documentsID:
        fileResponse = session.get('https://elearning.hs-offenburg.de/moodle/mod/resource/view.php?id=' + str(fileID),
                                   cookies=tastyCookie, stream=True)

        if fileResponse.status_code == 200:
            fileName = re.findall(r'"(.+)"', fileResponse.headers['Content-Disposition'].encode("iso-8859-1").decode('utf-8'))[0]
            print('Downloading: ' + fileName + ' ...')

            with open('/home/was_4/Documents/' + fileName, 'wb', os.O_CREAT) as f:
                f.write(fileResponse.content)
        else:
            print('Donwload failed!')

    session.close()


def failedLogin(site):
    return re.findall(r'class="loginform"', site)


if __name__ == '__main__':
    (username, password, saveLocation) = setupLogin()

    moodleStartpage = moodleLogin(username, password)
    downloadCourseFiles('https://elearning.hs-offenburg.de/moodle/course/view.php?id=2625')
    exit(0)

    Tools.createDirectory(saveLocation)

    crawlCourses(moodleStartpage)


#'please provide password for your moodle-account: '
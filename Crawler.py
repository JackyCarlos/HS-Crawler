#!/usr/bin/env python3

import requests
import re
import os
import Tools

loginPage = 'https://elearning.hs-offenburg.de/moodle/login/index.php'
moodleHost = 'https://elearning.hs-offenburg.de/'
tastyCookie = {}
ignoredCourses = [1643] # Brückenkurs


def moodleLogin(username, password):
    session = requests.session()

    try:
        hsPage = session.get(loginPage).text

        # in order to login we have to submit a token. Every time we enter the page to login a new one gets generated.
        loginToken = re.findall(r'name="logintoken" value="([a-zA-Z0-9]*)"', hsPage)[0]

        loginCredentials = {'username': username, 'password': password, 'logintoken': loginToken}

        siteLogin = session.post(loginPage, data=loginCredentials).text
        tastyCookie.update(session.cookies.get_dict())

    except Exception:
        print('The moodle site appears to be down. Check your internet connection. ')
        exit(0)

    if failedLogin(siteLogin):
        print('invalid login credentials')

        exit(0)

    session.close()

    return siteLogin


def failedLogin(site):
    return re.findall(r'class="loginform"', site)


def extractDocuments(coursePage):
    documentsID = re.findall(r'/mod/resource/view\.php\?id=([0-9]*)', coursePage)

    if 'forcedownload' in coursePage:
        additionalDocuments = re.findall(r'pluginfile\.php/([0-9]+)/mod_folder/content/0/(.{1,100})\?forcedownload=', coursePage)
        documentsID.extend(additionalDocuments)

    return documentsID


def downloadCourseFiles(url, savePath):
    session = requests.session()
    coursePage = session.get(url, cookies=tastyCookie).text
    i = 1

    courseName = re.findall(r'<title>.+: (.+)</title>', coursePage)

    if not courseName:
        return

    courseName = courseName[0].replace('/', '-').replace('\\', '-')
    courseFolder = os.path.join(savePath, courseName)
    os.mkdir(courseFolder)

    subFolders = re.findall(r'/mod/folder/view\.php\?id=([0-9]+)">', coursePage)

    if 'mod/folder/view.php' not in url:
        for folderID in subFolders:
            downloadCourseFiles(moodleHost + 'moodle/mod/folder/view.php?id=' + str(folderID), courseFolder)

    documentsIDs = extractDocuments(coursePage)

    #print(documentsIDs)

    print('Downloading files from ' + courseName)
    print((len(courseName) + 23) * '-')

    # https://elearning.hs-offenburg.de/moodle/pluginfile.php/404801/mod_folder/content/0/Vorlesungsunterlagen_Prozessmanagement_SS2019.pdf?forcedownload=1

    for fileID in documentsIDs:
        if type(fileID) is tuple:
            fileResponse = session.get(moodleHost + 'moodle/pluginfile.php/'
                                       + fileID[0] + '/mod_folder/content/0/' + fileID[1] + '?forcedownload=1',
                                       cookies=tastyCookie, stream=True)
        else:
            fileResponse = session.get(moodleHost + '/moodle/mod/resource/view.php', params={'id': fileID},
                                       cookies=tastyCookie, stream=True)

        if fileResponse.status_code == 200:
            if 'Content-Disposition' in fileResponse.headers:
                fileName = re.findall(r'"(.+)"', fileResponse.headers['Content-Disposition'].encode('iso-8859-1').decode('utf-8'))[0]
            else:
                fileName = 'Document-' + str(i)
                i += 1

            print('Downloading: ' + fileName + ' ...')

            with open(os.path.join(courseFolder, fileName), 'wb', os.O_CREAT) as f:
                f.write(fileResponse.content)
        else:
            print('Donwload failed!')

    session.close()

    print('\n\n')


def crawlCourses(moodleStartPage):
    savePath = Tools.createDirectory()
    courses = Tools.removeDuplicates(re.findall(r'course/view\.php\?id=([0-9]{4,})"', moodleStartPage))

    for course in courses:
        if course not in ignoredCourses:
            downloadCourseFiles(moodleHost + 'moodle/course/view.php?id=' + str(course), savePath)


if __name__ == '__main__':
    (username, password) = Tools.setupLogin()

    moodleStartpage = moodleLogin(username, password)

    crawlCourses(moodleStartpage)

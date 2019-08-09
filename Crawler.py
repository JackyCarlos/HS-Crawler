import requests
import os
import re
import datetime

loginPage = 'https://elearning.hs-offenburg.de/moodle/login/index.php'


def setupLogin(username, password):
    session = requests.session()

    try:
        hsPage = session.get(loginPage).text

        # in order to login we have to submit a token. Every time we enter the page to login a new one gets generated.
        token = re.findall(r'name="logintoken" value="([a-zA-Z0-9]*)"', hsPage)[0]

        loginCredentials = {'username': username, 'password': password, 'logintoken': token}

        siteLogin = session.post(loginPage, data=loginCredentials).text

    except Exception:
        print('The moodle site appears to be down. Check your internet connection. ')
        exit(0)

    # check for a failed login atempt
    if re.findall(r'class="loginform"', siteLogin):
        print('invalid login credentials')

        exit(0)

    return siteLogin


def crawlCourses(session, moodleStartPage):
    courses = removeDuplicates(re.findall(r'course/view\.php\?id=([0-9]{4,})"', moodleStartPage))

    print(courses)


def createDirectory(saveLocation):
    workingDirectory = os.path.expanduser('~') + '/' + saveLocation[2:]

    if not re.match(r'~/', saveLocation) or not os.path.isdir(workingDirectory):
        print('invalid saving location!')

        exit(0)

    newFolder = 'Moodle Download - ' + datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    print('Creating folder "' + newFolder + '" at "' + workingDirectory + '"')

    try:
        os.mkdir(workingDirectory + '/' + newFolder)
    except FileExistsError:
        print('Folder already exists - check your filesystem!')
    except OSError:
        print('Error - leaving')


def removeDuplicates(courses):
    courseList = []

    for course in courses:
        if course not in courseList:
            courseList.append(course)

    return courseList


if __name__ == '__main__':
    print('This tool logs into the moodle account you specify and downloads all the files within the courses and saves'
          'them to a folder of your choice.')

    username = input('please provide username for your moodle-account: ')
    password = input('please provide password for your moodle-account: ')
    saveLocation = input('please specify a location in your home directory starting with \'~/\': ')

    moodleStartpage = setupLogin(username, password)
    createDirectory(saveLocation)

    crawlCourses(moodleStartpage)



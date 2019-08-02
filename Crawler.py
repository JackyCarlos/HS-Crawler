import requests
import os
import re


def login():
    print('This tool logs into the moodle account you specify and downloads all the files within the courses and saves'
          'them to a folder of your choice.')

    username = input('please provide username for your moodle-account: ')
    password = input('please provide password for your moodle-account: ')
    saveLocation = input('please specify a location in your home directory starting with \'~\': ')

    # create a directory to safe the data to.
    createDirectory(saveLocation)

    exit(0)

    session = requests.session()
    hsPage = session.get('https://elearning.hs-offenburg.de/moodle/login/index.php').text

    # in order to login we have to submit a token. Every time we enter the page to login a new one gets generated.
    token = re.findall(r'name="logintoken" value="([a-zA-Z0-9]*)"', hsPage)

    loginCredentials = {'username': username, 'password': password, 'logintoken': token[0]}

    siteLogin = session.post('https://elearning.hs-offenburg.de/moodle/login/index.php', data=loginCredentials).text

    # check for a failed login atempt
    if re.findall(r'class="loginform"', siteLogin):
        print('invalid login credentials')

        return

    crawl(session, siteLogin)


def crawl(session, moodleStartPage):
    courses = removeDuplicates(re.findall(r'course/view\.php\?id=([0-9]{4,})"', moodleStartPage))

    print(courses)


def createDirectory(saveLocation):
    if not os.path.isdir(saveLocation) and not re.match(r'~', saveLocation):
        print('invalid saving location!')

        exit(0)

    homeDirectory = os.path.expanduser('~')
    print(homeDirectory)
    print(os.getcwd())



def removeDuplicates(courses):
    courseList = []

    for course in courses:
        if course not in courseList:
            courseList.append(course)

    return courseList


if __name__ == '__main__':
    login()


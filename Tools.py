#!/usr/bin/env python3

import os
import datetime
import re
import requests


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
    session = requests.session()

    fileResponse = session.get('http://www.pdf995.com/samples/pdf.pdf')

    print(fileResponse.headers)
    '''
    if fileResponse.status_code == 200:
        with open('/home/was_4/Documents/try.pdf', 'wb', os.O_CREAT) as f:
            f.write(fileResponse.content)
    '''


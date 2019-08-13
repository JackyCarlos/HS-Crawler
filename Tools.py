#!/usr/bin/env python3

import os
import datetime
import re


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
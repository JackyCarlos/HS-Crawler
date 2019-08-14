#!/usr/bin/env python3

import os
import datetime
import re
import requests


def createDirectory():
    print('files are downloaded to ~/Documents/<Moodle Download date:time>')

    workingDirectory = os.path.join(os.path.expanduser('~'), 'Documents')

    if not os.path.isdir(workingDirectory):
        print('invalid saving location!')

        exit(0)

    newFolder = 'Moodle Download - ' + datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    print('Creating folder "' + newFolder + '" at "' + workingDirectory + '"')

    path = os.path.join(workingDirectory, newFolder)

    try:
        os.mkdir(path)
    except FileExistsError:
        print('Folder already exists - check your filesystem!')
        exit(0)
    except OSError:
        print('Error - leaving')
        exit(0)

    return path


def removeDuplicates(courses):
    courseList = []

    for course in courses:
        if course not in courseList:
            courseList.append(course)

    return courseList


if __name__ == '__main__':
    print(r'\n')


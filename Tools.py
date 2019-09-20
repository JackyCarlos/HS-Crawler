#!/usr/bin/env python3

import os
import datetime
import getpass


def setupLogin():
    print('\nThis tool logs into the moodle account you specify and downloads all the files within the courses and saves'
          ' them to a folder located at ~/Documents \n')

    username = input('please provide username for your moodle-account: ')
    password = getpass.getpass('please provide password for your moodle-account: ')

    return username, password


def createDirectory():
    workingDirectory = os.path.join(os.path.expanduser('~'), 'Dokumente')

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

    print('files are downloaded to ' + path)

    return path


def removeDuplicates(courses):
    courseList = []

    for course in courses:
        if course not in courseList:
            courseList.append(course)

    return courseList

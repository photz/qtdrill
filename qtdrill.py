#!/usr/bin/env python

import sys
from PyQt4 import QtGui

from drillsergeant import DrillSergeant
from gui import Gui
import re
import codecs
import argparse
import logging
import string
import os


logging.basicConfig(level=logging.INFO)

class CannotParseLineException(Exception):
    pass

            
def get_labelfile_path(audiofile_path):
    path, ext = os.path.splitext(audiofile_path)

    expected_labelfile_extension = 'txt'

    return path + '.' + expected_labelfile_extension

def comma_separated_decimal_to_float(comma_separated_decimal,
                                     delimiter=','):

    if comma_separated_decimal.count(delimiter) != 1:
        raise Exception('improper format')

    return float(comma_separated_decimal.replace(delimiter, '.'))


def parse_label_line(line):

    regex = re.compile('(?P<start>\d+,\d+)\t(?P<end>\d+,\d+)\t(?P<section>[^;]*);(?P<drill>[^;]*);(?P<text>.*)')

    x = regex.match(line)

    if x == None:
        raise CannotParseLineException('the line given does not have the right format')


    return {
        'start_s' : comma_separated_decimal_to_float(x.group('start')),
        'end_s' : comma_separated_decimal_to_float(x.group('end')),
        'section' : x.group('section'),
        'drill' : x.group('drill'),
        'text' : x.group('text')
    }

    

def parse_labelfile(labelfile):

    lines = labelfile.readlines()
    
    logging.info('%d labels have been found.' % len(lines))

    
    exercises = {}

    for line_no, line in enumerate(lines):

        try:
            exercise = parse_label_line(line)
        except CannotParseLineException:
            logging.info('skipping line %d because it could not be parsed: %s' % (line_no, line))
        else:
            if not exercises.has_key(exercise['section']):
                exercises[exercise['section']] = {}

            if not exercises[exercise['section']].has_key(exercise['drill']):
                exercises[exercise['section']][exercise['drill']] = []

            exercises[exercise['section']][exercise['drill']].append(exercise)
    
    return exercises



def main():

    arg_parser = argparse.ArgumentParser(description=u'')

    arg_parser.add_argument('audiofiles',
                            type=str,
                            help='path to the audio file',
                            nargs='+')

    arg_parser.add_argument('--gui',
                            type=bool,
                            default=False)

    arg_parser.add_argument('--wait',
                            type=float,
                            help='length of the interval (in seconds) \
                            during which the student is expected \
                            to respond',
                            default=5)

    arg_parser.add_argument('--reps',
                            type=int,
                            help='repetitions of the correct answer',
                            default=2)

    arg_parser.add_argument('--html',
                            type=str,
                            help='only export to html and quit')

    arg_parser.add_argument('--wait-after-answer',
                            type=float,
                            help='time to wait (in seconds) after \
                            the correct answer is given',
                            default=1.0)

    try:
        args = arg_parser.parse_args()
    except Exception as x:
        print 'incorrect arguments'
        return

    exercises = []


    for audiofile_path in args.audiofiles:

        if not os.path.exists(audiofile_path) \
           or not os.path.isfile(audiofile_path):
            logging.error('%s does not point to a file' % audiofile_path)
            return

        labelfile_path = get_labelfile_path(audiofile_path)

        if not os.path.exists(labelfile_path) or \
           not os.path.isfile(labelfile_path):
            logging.error("unable to find the file containing the labels (expected at %s)" % labelfile_path)
            return

        with codecs.open(labelfile_path, 'r', encoding='utf-8') as labelfile:
            exercises.append((audiofile_path, parse_labelfile(labelfile)))

    if args.html:
        #os.path.exists(args.html):
        export_html(exercises, args.html)
        return

    if len(exercises) == 0:
        logging.info('no exercises have been found, quitting')
        return
    
    app = QtGui.QApplication(sys.argv)
    gui = Gui()

    drill_sergeant = DrillSergeant(gui, exercises)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

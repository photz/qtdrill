#!/usr/bin/env python3

import sys
from PyQt4 import QtGui

from labelled_audiofile import LabelledAudiofile
from yamlfile import YamlFile
from drillsergeant import DrillSergeant
from gui import Gui
from simplelabelfile import SimpleLabelFile


import codecs
import argparse
import logging
import string
import os


logging.basicConfig(level=logging.DEBUG)
def get_args():

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
        print('incorrect arguments')
        return

    return args



def main():
    args = get_args()

    drill_sections = list()

    label_file_type = SimpleLabelFile

    handlers = {
        '.flac' : label_file_type,
        '.mp3' : label_file_type,
        '.wav' : label_file_type,
        '.yaml' : YamlFile
    }

    for audiofile_path in args.audiofiles:

        _, ext = os.path.splitext(audiofile_path)

        if ext not in handlers:
            logging.error('no handler for {}.'.format(ext))
            raise Exception('unknown file extension {}'.format(ext))

        af = handlers[ext](audiofile_path)

        try:
            af.parse()
        except Exception as e:
            logging.error('could not parse %s' % audiofile_path)
            raise e
        else:
            drill_sections.extend(af.get_drill_sections())
        
    logging.info('a total of %d drill section have been found'
                 % len(drill_sections))


    app = QtGui.QApplication(sys.argv)
    gui = Gui()

    drill_sergeant = DrillSergeant(gui, drill_sections)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
import mutagen.id3
from random import choice
import logging
import string
import subprocess
import os

PATH_TO_AUDIO_PLAYER = 'mpv'


def play_section(path_to_audio_file, start_s, length_s):
    assert os.path.exists(path_to_audio_file)
    assert os.path.isfile(path_to_audio_file)

    start_at_arg = '--start=%f' % start_s

    length_arg = '--length=%f' % length_s

    args = [
        PATH_TO_AUDIO_PLAYER,
        start_at_arg,
        length_arg,
        path_to_audio_file
    ]
            
    logging.debug(string.join(args, ' '))

    with open(os.devnull, 'w') as silent:
        subprocess.call(args, stdout=silent, stderr=silent)



class DrillSergeant(object):

    SUCCESSIVE_DRILLS_PER_SECTION = 10

    def __init__(self, gui, exercises):

        self.gui = gui
        self.exercises = exercises
        self.section = None
        self.exercise = None

        # the number of drills we've gone through from the current
        # section successively
        # this counter is reset whenever a new section is chosen
        self.section_drill_counter = 0

        gui.set_uncover_callback(self.uncover)

        gui.set_next_callback(self.set_next)

        gui.set_play_student_again_callback(self.play_student_again)

        gui.set_play_teacher_again_callback(self.play_teacher_again)

    def uncover(self):
        if self.exercise and len(self.exercise) > 1:
            self.gui.set_student(self.exercise[1]['text'])
            self.play_student_audio()
        else:
            logging.warning('no exercise')

    def set_next(self):


        if not self.section \
           or self.section_drill_counter > DrillSergeant.SUCCESSIVE_DRILLS_PER_SECTION:

            self.audiofile_path, self.exercise_set = \
                                            choice(self.exercises)

            self.section = choice(self.exercise_set.values())
            self.section_drill_counter = 0


        assert self.section
        assert self.audiofile_path

        self.exercise = choice(self.section.values())
        


        self.gui.set_source('%s <b>%d</b> of <b>%d</b>'
                            % (self.audiofile_path,
                               self.section_drill_counter,
                               len(self.section)))



        self.play_teacher_audio()
        self.gui.set_teacher(self.exercise[0]['text'])

        self.gui.set_student('')

        self.section_drill_counter += 1

    def play_teacher_again(self):
        if self.exercise:
            self.play_teacher_audio()
        else:
            logging.warning('no exercise selected')

    def play_student_again(self):
        if self.exercise:
            self.play_student_audio()
        else:
            logging.warning('no exercise selected')


    def play_teacher_audio(self):
        play_section(self.audiofile_path,
                     self.exercise[0]['start_s'],
                     self.exercise[0]['end_s'] - self.exercise[0]['start_s'])

    def play_student_audio(self):
        play_section(self.audiofile_path,
                     self.exercise[1]['start_s'],
                     self.exercise[1]['end_s'] - self.exercise[1]['start_s'])    

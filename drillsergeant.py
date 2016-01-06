from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
import mutagen.id3
from random import choice, shuffle, random
import logging
import string
import os
from utils import play_section


class DrillDirection(object):
    normal = 0
    reverse = 1

class DrillSergeant(object):

    def __init__(self, gui, exercises):

        self._reverse_likelihood = 0.3
        self._shuffle_drills = True

        self.gui = gui
        self.exercises = exercises

        self.current_section = None
        self.current_drill = None
        self._current_direction = None

        # the number of drills we've gone through from the current
        # section successively
        # this counter is reset whenever a new section is chosen
        self.section_drill_counter = 0

        gui.set_uncover_callback(self.uncover)

        gui.set_next_callback(self.set_next)

        gui.set_play_student_again_callback(self.play_student_again)

        gui.set_play_teacher_again_callback(self.play_teacher_again)

        gui.set_skip_remaining_callback(self.skip_remaining)

    def _get_current_teacher(self):
        if self._current_direction is DrillDirection.normal:
            return self.current_drill[0]
        else:
            return self.current_drill[1]

    def _get_current_student(self):
        if self._current_direction is DrillDirection.normal:
            return self.current_drill[1]
        else:
            return self.current_drill[0]


    def skip_remaining(self):
        self._choose_new_section()
        self.set_next()

    def uncover(self):
        if self.current_drill and len(self.current_drill) > 1:
            self.gui.set_student(self._get_current_student()['text'])
            self.play_student_again()
        else:
            logging.warning('no exercise')

    def _choose_new_section(self):



        assert 0 <= self._reverse_likelihood \
            and self._reverse_likelihood <= 1.0

        # throw a dice
        if self._reverse_likelihood < random():
            self._current_direction = DrillDirection.normal
        else:
            self._current_direction = DrillDirection.reverse

        self.audiofile_path, exercise_set = choice(self.exercises)

        section = choice(exercise_set.values())

        self.current_section = list(section.values())

        if self._shuffle_drills:
            shuffle(self.current_section)

    def _current_section_has_drills_left(self):
        return self.current_section and len(self.current_section) > 0


    def _set_next_drill_in_current_section(self):
        assert self.current_section
        assert len(self.current_section) > 0

        self.current_drill = self.current_section.pop()

    def set_next(self):

        if not self._current_section_has_drills_left():

            self._choose_new_section()            

        self._set_next_drill_in_current_section()

        self.gui.set_source('%s, %d drills left'
                            % (self.audiofile_path,
                               len(self.current_section)))

        self.gui.set_student('')

        self.play_teacher_again()
        self.gui.set_teacher(self._get_current_teacher()['text'])


    def play_teacher_again(self):
        if not self.current_drill:
            return

        self._play(self.audiofile_path, self._get_current_teacher())

        

    def play_student_again(self):
        if not self.current_drill:
            return

        self._play(self.audiofile_path, self._get_current_student())


    @staticmethod
    def _play(audio, drill):

        play_section(audio,
                     drill['start_s'],
                     drill['end_s'] - drill['start_s'])


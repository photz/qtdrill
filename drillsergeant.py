from random import choice, shuffle, random
import logging
import string
import os
from utils import play_section
from drill_section import DrillSection

class DrillDirection(object):
    normal = 0
    reverse = 1

class DrillSergeant(object):

    def __init__(self, gui, drill_sections):

        self._reverse_likelihood = 0.3
        self._shuffle_drills = True

        self.gui = gui
        self._drill_sections = drill_sections

        self._current_section = None
        self._drills_queue = None
        self._current_drill = None
        self._current_direction = None

        # the number of drills we've gone through from the current
        # section successively
        # this counter is reset whenever a new section is chosen

        gui.set_uncover_callback(self.uncover)

        gui.set_next_callback(self.set_next)

        gui.set_play_student_again_callback(self.play_student_again)

        gui.set_play_teacher_again_callback(self.play_teacher_again)

        gui.set_skip_remaining_callback(self.skip_remaining)

        self._choose_new_section()

    def _get_current_teacher(self):
        if self._current_direction is DrillDirection.normal:
            return self._current_drill.get_teacher()
        else:
            return self._current_drill.get_student()

    def _get_current_student(self):
        if self._current_direction is DrillDirection.normal:
            return self._current_drill.get_student()
        else:
            return self._current_drill.get_teacher()


    def skip_remaining(self):
        self._choose_new_section()
        self.set_next()

    def uncover(self):
        if self._current_drill:
            self.gui.set_student(self._get_current_student().get_text())
            self.play_student_again()
        else:
            logging.warning('no exercise')

    def _choose_new_section(self):

        logging.debug('choosing a new section')

        assert 0 <= self._reverse_likelihood \
            and self._reverse_likelihood <= 1.0

        # throw a dice
        if self._reverse_likelihood < random():
            self._current_direction = DrillDirection.normal
        else:
            self._current_direction = DrillDirection.reverse


        self._current_section = choice(self._drill_sections)

        assert type(self._current_section) is DrillSection

        self._drills_queue = list(self._current_section.get_drills())

        if self._shuffle_drills:
            shuffle(self._drills_queue)

        if self._current_section.has_example():
            self._current_section.get_example().play()

    def _current_section_has_drills_left(self):
        return self._drills_queue != None and len(self._drills_queue) > 0


    def _set_next_drill_in_current_section(self):
        assert self._drills_queue
        assert len(self._drills_queue) > 0

        self._current_drill = self._drills_queue.pop()

    def set_next(self):

        assert len(self._drill_sections) > 0

        if not self._current_section_has_drills_left():

            self._choose_new_section()


        self._set_next_drill_in_current_section()

        self.gui.set_source('%d drills left'
                            % len(self._drills_queue))

        self.gui.set_student('')

        self.play_teacher_again()
        self.gui.set_teacher(self._get_current_teacher().get_text())


    def play_teacher_again(self):
        if not self._current_drill:
            return

        self._get_current_teacher().play()

    def play_student_again(self):
        if not self._current_drill:
            return

        self._get_current_student().play()

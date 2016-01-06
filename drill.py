class Drill(object):

    def __init__(self, teacher, student):

        self._teacher = teacher
        self._student = student

    def play_student(self):
        self._teacher.play()

    def play_teacher(self):
        self._student.play()

    def get_teacher(self):
        return self._teacher

    def get_student(self):
        return self._student

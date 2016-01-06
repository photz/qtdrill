import sys
from PyQt4 import QtGui, QtCore


class Gui(QtGui.QWidget):
    
    def __init__(self):
        self.teacher_label = None
        self.student_label = None

        super(Gui, self).__init__()
        
        self.initUI()
        
    def set_teacher(self, text):
        self.teacher_label.setText('<span style="font-size: 20pt;">' + text + '</span>')

    def set_student(self, text):
        self.student_label.setText('<span style="font-size: 20pt;">' + text + '</span>')

    def set_uncover_callback(self, cb):
        self.uncover_btn.clicked.connect(cb)

        self.connect(self.uncover_sc,
                     QtCore.SIGNAL('activated()'),
                     cb)

    def set_play_teacher_again_callback(self, cb):
        self.play_teacher_again_btn.clicked.connect(cb)

        self.connect(self.play_teacher_again_sc,
                     QtCore.SIGNAL("activated()"),
                     cb)


    def set_source(self, source):
        self.source_label.setText(source)

    def set_play_student_again_callback(self, cb):
        self.play_student_again_btn.clicked.connect(cb)

        self.connect(self.play_student_again_sc,
                     QtCore.SIGNAL("activated()"),
                     cb)


    def set_next_callback(self, cb):
        self.next_btn.clicked.connect(cb)

        self.connect(self.next_sc,
                     QtCore.SIGNAL('activated()'),
                     cb)

    def set_skip_remaining_callback(self, cb):
        self.skip_remaining_btn.clicked.connect(cb)

        self.connect(self.skip_remaining_sc,
                     QtCore.SIGNAL('activated()'),
                     cb)


    def initUI(self):
        grid = QtGui.QGridLayout(self)


        self.source_label = QtGui.QLabel('')
        grid.addWidget(self.source_label, 0, 0, 1, 5)
        

        self.teacher_label = QtGui.QTextEdit()
        self.teacher_label.setAlignment(QtCore.Qt.AlignCenter)


        grid.addWidget(self.teacher_label, 1, 0, 1, 5)


        self.student_label = QtGui.QTextEdit()
        self.student_label.setAlignment(QtCore.Qt.AlignCenter)

        grid.addWidget(self.student_label, 2, 0, 1, 5)


        self.uncover_btn = QtGui.QPushButton('uncover')
        grid.addWidget(self.uncover_btn, 3, 0)

        self.uncover_sc = QtGui.QShortcut(self.uncover_btn)
        self.uncover_sc.setKey('SPACE')


        # play again button and its shortcut for the
        # part said by the teacher

        self.play_teacher_again_btn = QtGui.QPushButton('play teacher')
        grid.addWidget(self.play_teacher_again_btn, 3, 1)

        self.play_teacher_again_sc = \
                        QtGui.QShortcut(self.play_teacher_again_btn)
        self.play_teacher_again_sc.setKey('T')

        # play again button and its shortcut for the
        # part said by the student

        self.play_student_again_btn = QtGui.QPushButton('play student')
        grid.addWidget(self.play_student_again_btn, 3, 2)

        self.play_student_again_sc = \
                        QtGui.QShortcut(self.play_student_again_btn)
        self.play_student_again_sc.setKey('S')

        # next button

        self.next_btn = QtGui.QPushButton('next')
        grid.addWidget(self.next_btn, 3, 3)
        self.next_sc = QtGui.QShortcut(self.next_btn)
        self.next_sc.setKey('N')

        # skip remaining

        self.skip_remaining_btn = QtGui.QPushButton('skip remaining')
        grid.addWidget(self.skip_remaining_btn, 3, 4)
        self.skip_remaining_sc = QtGui.QShortcut(self.skip_remaining_btn)
        self.skip_remaining_sc.setKey('Z')

        # window

        self.setWindowTitle('QtDrill')
    
        self.show()
        
        



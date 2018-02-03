# -*- coding: UTF-8 -*-

import pickle
import os
import os.path
import time

folder = '/Users/william/Python/'

class Assistant:
    # Assistant Class
    def __init__(self, name='expert', data=None):
        self.name = name
        self.data = data
        self.saveflag = False
        # self.memory = []
        self.description = 'I am an object of Assistant class'
        self.type_ = '.pkl'
        self.folder = folder

    # save and load:
    @staticmethod
    def load(filename):
        with open(filename, 'rb') as fo:
            return pickle.load(fo)

    def save(self, filename=None):
        if filename is None:
            filename = self.folder + self.name + self.type_
        if self.saveflag is True:
            self.saveflag = False
            with open(filename, 'wb') as fo:
                pickle.dump(self, fo)

    def __getstate__(self):
        return self.name, self.data

    def __setstate__(self, state):
        self.name, self.data = state

    def parse(self, question):
        # overriden in subclasses
        return question

    def answer(self, question):
        # implemented in subclasses
        # question -> answer
        raise NotImplementedError

    def update(self, question, answer):
        # get local time
        self.saveflag = True

    def welcome(self):
        return 'I am %s, Can I help you? (input [q]uit to quit)'%self.name

    def ask_to_update(self):
        return 'Are you content with my answer? If not, show me the right answer.'

    def ask_to_save(self):
        return 'Do you want to save the new data?'

    def farewell(self):
        return 'Goodbye.'

    def ask(self):
        return 'Tell me what is your question.'


class Answer(object):
    '''Answer has 3 (principal) propteries
    content: content
    last_time: last time
    reference: reference'''
    def __init__(self, content, last_time=None, reference=''):
        self.content = content
        self.last_time = time.asctime() if last_time is None else last_time
        self.reference = reference

    def __str__(self):
        return '%s[last time:%s]'%(self.content, self.last_time)

    def __repr__(self):
        return 'answer: %s[last time:%s]\n also see: %s'%(self.content, self.last_time, self.reference)


class Controler:
    '''Controler Class'''

    def __init__(self, prompt1='--', prompt2='--'):
        self.prompt1 = prompt1
        self.prompt2 = prompt2
        self.history = []

    def print_(self, s=''):
        print(self.prompt1, s)

    def input_(self):
        return input(self.prompt2 + ' ')

    def respond(self, request='', callback=None):
        if callable:
            callback()

    def start(self):
        print('Welcome, my host.')

    def end(self):
        print('The conversation is completed.')


    def run(self, assistant):
        self.start()
        self.print_(assistant.welcome())
        if self.input_() in {'yes', 'y', 'Yes', 'Y'}:
            while True:
                self.print_(assistant.ask())
                q = self.input_()
                if q in {'q', 'quit'}:
                    break
                result = assistant.parse(q)
                self.print_(assistant.answer(result))
                self.print_(assistant.ask_to_update())
                s = self.input_()
                if s in {'yes', 'y', 'Yes', 'Y'}:
                    continue
                assistant.update(q, Answer(s))
            self.print_(assistant.ask_to_save())
            s = self.input_()
            if s in {'yes', 'y', 'Yes', 'Y'}:
                assistant.save()
                self.print_(assistant.farewell())
        self.end()


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Window(QMainWindow):
    def __init__(self, assistant, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.assistant = assistant

        self.setWindowTitle('come on, bro!')
        self.timer = QBasicTimer()
        self.step = 0

        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        lname = QLabel(assistant.name)
        layout1.addWidget(lname)
        self.respond = QTextEdit()
        layout1.addWidget(self.respond)

        layout2 = QHBoxLayout()
        lname = QLabel(assistant.name)
        layout2.addWidget(lname)
        self.request = QTextEdit()
        layout2.addWidget(self.request)
        btn = QPushButton('Submit')
        btn.pressed.connect(self.submit)
        layout2.addWidget(btn)

        layout.addLayout(layout1)
        layout.addLayout(layout2)

        bsave = QPushButton('Save')
        bsave.pressed.connect(self.save)
        layout1.addWidget(bsave)
        bquit = QPushButton('Quit')
        bquit.pressed.connect(self.quit)
        layout1.addWidget(bquit)

        # window: widget(layout(layout1, layout2))
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    def submit(self):
        self.request.text()
        result = assistant.parse(q)
        self.respond.setText(self.assistant.answer(result))
        self.respond.setText(self.assistant.ask_to_update())

    def save(self):
        self.assistant.save()

    def quit(self):
        reply = QMessageBox.information(self, "Quit", "Do you Want to save the data?", QMessageBox.Yes | QMessageBox.No) 
        if reply:
            self.assistant.save()


class Command(object):
    '''Command has 2 (principal) propteries
    name: name
    action: action'''
    def __init__(self, name, action):
        self.name = name
        self.action = action

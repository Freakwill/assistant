#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

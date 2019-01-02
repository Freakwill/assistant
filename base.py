#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Create an assistant for yourself

In MVC pattern
"""

import pickle
import time
import pathlib

DEFAULT_FOLDER = pathlib.Path('~').expanduser()

class Assistant:
    """An extensible expert system.

    Implement answer/update methods in subclasses.
    """
    folder = DEFAULT_FOLDER

    def __init__(self, name='expert', data=None, description='I am an object of Assistant class'):
        self.name = name
        self.data = data
        self.saveflag = False
        # self.memory = []
        self.description = description

    @classmethod
    def create(cls, name, *args, **kwargs):
        # Create an assistant, if it exists, then just load it.
        filename = (cls.folder / name).with_suffix('.pkl')
        if filename.exists():
            print('[Assistant %s is loaded]' % name)
            return Assistant.load(filename)
        else:
            print('[New assistant %s is created]' % name)
            return cls(name, *args, **kwargs)

    # save/load methods:
    @staticmethod
    def load(filename):
        with open(filename, 'rb') as fo:
            return pickle.load(fo)

    def save(self, filename=None):
        if filename is None:
            filename = (self.folder / self.name).with_suffix('.pkl')
        if self.saveflag is True:
            self.saveflag = False
            with open(filename, 'wb') as fo:
                pickle.dump(self, fo)

    def __setstate__(self, state):
        self.name, self.data, self.description = state['name'], state['data'], state['description']

    def reset(self):
        self.data = None

    def parse(self, question):
        # overridden in subclasses
        return question

    def answer(self, question):
        # implemented in subclasses
        # question -> answer
        raise NotImplementedError

    def respond(self, question):
        """Respond your question

        The main method of the class
        
        Arguments:
            question {str} -- the string of question
        
        Returns:
            str
        """
        return self.answer(self.parse(question))

    def update(self, question, answer):
        raise NotImplementedError

    # Some polite expressions
    def welcome(self):
        return 'I am %s, Can I help you? (input [q]uit to quit)' % self.name

    def farewell(self):
        return 'Goodbye.'

    def ask(self):
        return 'What is your question?'


class Answer:
    """Answer given by your assistant

    Essentially, it is a string with time.
    """
    def __init__(self, content, last_time=None):
        self.content = content
        self.last_time = time.asctime() if last_time is None else last_time

    def __str__(self):
        return '%s[last time:%s]'%(self.content, self.last_time)

    def __repr__(self):
        return 'answer: %s[last time:%s]'%(self.content, self.last_time)

    def __bool__(self):
        return self.content and self.content != "I don't know."

    def __setstate__(self, state):
        self.content, self.last_time = state['content'], state['last_time']


class Controller:
    """Controller Class

    Interface via which clients communicate with their assistants.
    """

    def __init__(self, prompt1='--', prompt2='--'):
        """
        Keyword Arguments:
            prompt1 {str} -- [assistant's prompt] (default: {'--'})
            prompt2 {str} -- [user's prompt] (default: {'--'})
        """
        self.prompt1 = prompt1
        self.prompt2 = prompt2
        self.history = []
        self.commands = {}

    def print_(self, s=''):
        print(self.prompt1, s)

    def input_(self, repeat=False):
        inp = input(self.prompt2 + ' ')
        if repeat:
            if inp == '':
                inp = self.input_(repeat)
        return inp

    def register_command(self, name, action):
        self.commands.update({name: action})

    def __getitem__(self, key):
        return self.commands[key]

    def __enter__(self):
        print('Welcome, my host.')
        return self

    def __exit__(self, *args, **kwargs):
        self.history = []
        print('The controller is shut down.')


    def run(self, assistant):
        self.print_(assistant.welcome())
        if self.input_() in {'yes', 'y', 'Yes', 'Y', ''}:
            while True:
                self.print_(assistant.ask())
                q = self.input_()
                if q in {'q', 'quit'}:
                    self.print_(assistant.farewell())
                    break
                if q.startswith('%'):
                    cmd = q.lstrip('% ')
                    if cmd in self.commands:
                        self[cmd](assistant, self.history)
                    elif hasattr(assistant, cmd):
                        getattr(assistant, cmd)()
                else:
                    self.history.append(q)
                    self.print_(assistant.respond(q))
                    self.print_('Are you satisfied with the answer?[Press enter for yes] If not, show the right answer.')
                    s = self.input_()
                    if s:
                        assistant.update(q, Answer(s))
                        assistant.saveflag = True
                        continue
                    self.print_('^_^')

            s = input('Do you want to save the new data?[y/n]')
            if s in {'', 'y', 'yes'}:
                self.save(assistant)
                print('data are saved.')
        else:
            self.print_(assistant.farewell())

    def save(self, assistant):
        assistant.save()


class SimpleAssistant(Assistant):
    """Essentially, it is a dict
    
    The answer method is `get` method of dict.
    The update method is `update` method of dict.
    """
    def __init__(self, name='Simple', data=None, *args, **kwargs):
        if data is None:
            data = {}
        super(SimpleAssistant, self).__init__(name, data, *args, **kwargs)

    def reset(self):
        self.data = {}

    def answer(self, question):
        # question -> answer
        return self.data.get(question, Answer("I don't know."))

    def update(self, question, answer):
        if isinstance(answer, str):
            answer = Answer(answer)
        answer.last_time = time.asctime()
        self.data.update({question:str(answer)})


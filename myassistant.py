# -*- coding: UTF-8 -*-

import pickle
import os
import os.path
import time

import assistant

class SimpleAssistant(assistant.Assistant):

    def __init__(self, name='Simple', data={}):
        super(SimpleAssistant, self).__init__(name, data)

    def answer(self, question):
        # implemented in subclasses
        # question -> answer
        return self.data.get(question, assistant.Answer("I don't know."))

    def update(self, question, answer):
        if isinstance(answer, str):
            answer = assistant.Answer(answer)
        t = time.asctime()
        answer.last_time = t
        self.data.update({question:str(answer)})
        self.saveflag = True


class MathAssistant(SimpleAssistant):

    root = '/Users/william/Folders/笔记/'

    def search(self, question):
        return self.search_local()

    def search_local(self, question):
        res = []
        for parent, dirnames, filenames in os.walk(MathAssistant.root):
            for filename in filenames:
                if os.path.splitext(filenames)[-1] in {'.md', '.tex'}:
                    fullname = join(parent, filename)
                    with open(fullname) as fo:
                        s = fo.read()
                        if question in s:
                            res.append(fullname)
        return res




class PythonAssistant(SimpleAssistant):
    pass



if __name__ == '__main__':

    c = assistant.Controler()
    sa = SimpleAssistant('Lisa')
    c.run(sa)
    sa = SimpleAssistant.load('/Users/william/Python/Lisa.pkl')
    c.run(sa)
    
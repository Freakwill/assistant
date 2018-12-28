# -*- coding: UTF-8 -*-

import pathlib

import assistant
import wikipedia
wikipedia.exceptions.PageError

class WebAssistant(assistant.SimpleAssistant):
    pass


class WikiAssistant(WebAssistant):

    def answer(self, question):
        # question -> answer
        a = super(WikiAssistant, self).answer(question)
        if a:
            return a
        try:
            return wikipedia.summary(question)
        except:
            raise wikipedia.exceptions.PageError(question)


with assistant.Controler() as c:
    lucy = WikiAssistant.create('Lucy')
    c.run(lucy)
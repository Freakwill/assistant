#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pathlib

import wikipedia
import yaml

import assistant

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

class YAMLAssistant(assistant.SimpleAssistant):
    """
    Save data in yaml files.
    """
    suffix = '.yaml'

    @staticmethod
    def load(filename):
        with open(filename) as fo:
            return yaml.load(fo)

    def save(self, filename=None):
        if filename is None:
            filename = (self.folder / self.name).with_suffix('.yaml')
        if self.saveflag is True:
            self.saveflag = False
            with open(filename, 'w') as fo:
                yaml.dump(self, fo)


if __name__ == '__main__':
    with assistant.Controller() as c:
        c.register_command('print', lambda x, y: print(x.data))
        a = YAMLAssistant.create('Yan')

        c.run(a)
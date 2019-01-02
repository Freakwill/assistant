#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pathlib

import assistant


class MathAssistant(assistant.SimpleAssistant):

    root = pathlib.Path('~/Folders/Math Note/').expanduser()

    def search(self, question):
        return self.search_local()

    def search_local(self, question, start=root):
        res = []
        for path in MathAssistant.root.iterdir():
            if path.suffix in {'.md', '.tex'}:
                s = path.read_text()
                if question in s:
                    res.append(path)
            elif path.is_dir():
                search_local(self, question, path)
        return res


class PythonAssistant(assistant.SimpleAssistant):
    pass
    
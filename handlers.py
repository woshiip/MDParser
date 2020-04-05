#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re


class HTMLHandler:
    def callback(self, type, *args):
        method = getattr(self, type, None)
        print(method)
        if callable(method):
            return method(*args)

    def title(self, block):
        group = re.match('(#{1,6}) (.*)', block)
        if group is None:
            return None
        prefix = group[1]
        text = group[2]
        level = len(prefix)
        start = "<h%d> " % level
        end = " </h%d>" % level
        block = start + text + end
        return block

    def listitem(self, block):
        print("in listitem handler")
        return re.sub(r'-( )+(.*)', r'<li> \2 </li>', block)

    def start_list(self, block):
        return '<ul> \n'

    def end_list(self, block):
        return '\n </ul> \n'

    def paragraph(self, block):
        block = '<p> ' + block + ' </p>'
        return block









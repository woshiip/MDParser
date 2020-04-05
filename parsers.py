#!/usr/bin/env python
# -*- coding:utf-8 -*-

from rules import *
from handlers import HTMLHandler
import re


class Parser:
    def __init__(self, handler):
        self.blocks = []
        self.handler = handler
        self.rules = []
        self.filters = []

    def add_rule(self, rule):
        self.rules.append(rule)

    # def add_filter(self, type):
    #     print("in add_filter")
    #     method = getattr(Filter, type, None)
    #     if callable(method):
    #         print("add filter ")
    #         self.filters.append(method)

    def add_filter(self, pattern, repl):
        def filter(block):
            return re.sub(pattern, repl, block)
        self.filters.append(filter)

    def parse(self, file):
        with open(file, 'r') as fd:
            for block in fd:
                if len(block.strip()) == 0:
                    continue
                print("-----------------------------------------")
                print(block)
                for i in self.parse_block(block.strip()):
                    yield i
        for i in self.parse_block('\n'):
            yield i

    def parse_block(self, block) -> str:
        if self.rules is None:
            raise Exception("empty rules")

        for i in self.filters:
            block = i(block)

        for i in self.rules:
            rule = i()
            print(rule.type)
            if rule.condition(block) == True:
                # block = rule.action(block, self.handler)
                yield rule.action(block, self.handler)
                if rule.passthrough == False:
                    break

        # block = '<p> ' + block + ' </p>'
        return block


class TextBasicParser(Parser):
    def __init__(self):
        Parser.__init__(self, HTMLHandler)
        self.add_rule(TitleRule)
        self.add_rule(ListRule)
        self.add_rule(ListItemRule)
        self.add_rule(ParagraphRule)
        # self.add_filter('bold')
        # self.add_filter('emphasis')
        self.add_filter(r'\*\*(.+?)\*\*', r'<b>\1</b>') # bold
        self.add_filter(r'\*(.+?)\*', r'<em>\1</em>') # emphasis
        self.add_filter(r'`([^`]+?)`', r'<code>\1</code>')  # code





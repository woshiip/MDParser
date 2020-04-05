#!/usr/bin/env python
# -*- coding:utf-8 -*-

from abc import abstractmethod
import re
from handlers import HTMLHandler


class Rule:
    type = "text"
    passthrough = True

    @abstractmethod
    def condition(self, block):
        raise Exception("not implement")

    def action(self, block, handler):
        return handler().callback(self.type, block)


class TitleRule(Rule):
    type = "title"
    passthrough = False

    def condition(self, block):
        if re.match('#{1,6} ', block):
            return True
        else:
            return False


class ListItemRule(Rule):
    type = "listitem"
    passthrough = False

    def condition(self, block):
        return block[0] == '-' and block[1] == ' '


class ListRule(ListItemRule):
    type = "list"
    passthrough = True
    inside = False

    def condition(self, block):
        print("inside:" + str(self.inside))
        if ListRule.inside is False and ListItemRule.condition(self, block):
            print('list begin')
            return True
        elif ListRule.inside and not ListItemRule.condition(self, block):
            print('list end')
            return True
        else:
            return False

    def action(self, block, handler):
        if ListRule.inside is False:
            ListRule.inside = True
            return handler().callback('start_' + self.type, block)
        else:
            ListRule.inside = False
            return handler().callback('end_' + self.type, block)


class ParagraphRule(Rule):
    type = 'paragraph'
    passthrough = False

    def condition(self, block):
        return True











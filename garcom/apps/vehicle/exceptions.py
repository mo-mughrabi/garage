# -*- coding: utf-8 -*-
'''

'''


class InternationalizationException(Exception):
    def __init__(self, message, Errors):

        Exception.__init__(self, message)

        self.Errors = Errors

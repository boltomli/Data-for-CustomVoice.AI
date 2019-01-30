#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''This module provides utilities'''
import nltk
from aeneas.language import Language


def allowed_languages():
    '''Allowed languages'''
    return Language.ALLOWED_VALUES


def download_punkt():
    '''Download punkt resource'''
    return nltk.download('punkt')

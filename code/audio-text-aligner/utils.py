#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''This module provides utilities'''
import nltk
from aeneas.language import Language


def allowed_languages():
    '''Allowed languages'''
    lang_dict = {}
    for item in Language.CODE_TO_HUMAN_LIST:
        lang_dict[item.split('\t')[0]] = item.split('\t')[1]
    return lang_dict


def download_punkt():
    '''Download punkt resource'''
    return nltk.download('punkt')

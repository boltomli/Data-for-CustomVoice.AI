#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''This module converts text encoding if necessary'''

import chardet
import codecs
import requests

def process_url(url, filename):
    '''From URL'''
    with open(filename, 'wb') as f:
        f.write(requests.get(url).content)
    return process_file(filename)

def process_file(filename):
    '''From file'''
    try:
        chardet.detect(open(filename, 'r').read())
    except UnicodeDecodeError:
        text = codecs.open(filename, 'r', encoding='gbk').read()
        with codecs.open(filename, 'w', encoding='utf_8') as f:
            f.write(text)
    finally:
        return filename

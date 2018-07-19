#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''This is the main module for the app'''

import argparse
from os import listdir
from os.path import isdir, isfile, join, exists
import chardet
import codecs

def process_script_file(script_file):
    '''Read script file file as text'''
    text_encoding = 'gbk'
    try:
        text_encoding = chardet.detect(open(script_file, 'r').read())['encoding']
    except UnicodeDecodeError:
        text_encoding = 'utf-16'
    text_content = codecs.open(script_file, 'r', encoding=text_encoding).readlines()
    return text_content

def process_script_line(script_item):
    '''
    Deal with one line of script in the format like:
    001\tI'm one line. Not necessarily one sentence.
    Drop if there're more than one Tab or the ID is not a number
    '''
    script_dict = {}
    script_item = script_item.strip()
    if '\t' in script_item:
        item = script_item.split('\t')
        if len(item) == 2 and item[0].isdigit():
            script_dict.update({item[0]: item[1]})
    return script_dict

def process_script_dict(script_dict, update_dict):
    '''Add if ID is not found. Remove if ID is found.'''
    for item in update_dict:
        if item in script_dict.keys():
            script_dict.pop(item)
        else:
            script_dict.update({item: update_dict[item]})
    return script_dict

def process_script(path):
    '''
    Process text file or files in folder into scripts
    Each script should have unique ID so duplicate IDs are removed
    '''
    script_dict = {}
    if isfile(path):
        text = process_script_file(path)
        for line in text:
            script_dict = process_script_dict(script_dict, process_script_line(line))
    else:
        for f in [join(path, f) for f in listdir(path) if isfile(join(path, f))]:
            text = process_script_file(f)
            for line in text:
                script_dict = process_script_dict(script_dict, process_script_line(line))
    return script_dict

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--wave',
                        help='Directory of wave files (*.wav).')
    parser.add_argument('--text',
                        help='Script file or directory of script files (*.txt).')

    args = parser.parse_args()

    if isdir(args.wave) and exists(args.text):
        script_dict = process_script(args.text)
        print(len(script_dict))
    else:
        parser.print_help()

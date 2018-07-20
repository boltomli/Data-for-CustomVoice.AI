#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''Match valid script ID and wave files to create batches to upload.'''

import argparse
import codecs
from os import walk
from os.path import exists, isdir, isfile, join, splitext

import chardet


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


def process_dict(script_dict, update_dict):
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
            script_dict = process_dict(script_dict, process_script_line(line))
    else:
        for r,d,f in walk(path):
            for filename in f:
                if splitext(filename)[1].lower() == '.txt':
                    text = process_script_file(join(r, filename))
                    for line in text:
                        script_dict = process_dict(script_dict, process_script_line(line))
    return script_dict


def process_wave(path):
    wave_dict = {}
    for r,d,f in walk(path):
        for filename in f:
            item = splitext(filename)
            if item[0].isdigit() and item[1].lower() == '.wav':
                wave_dict = process_dict(wave_dict, {item[0]: join(r, filename)})
    return wave_dict

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--wave',
                        default='data',
                        help='Directory of wave files (*.wav).')
    parser.add_argument('--text',
                        default='data',
                        help='Script file or directory of script files (*.txt).')

    args = parser.parse_args()

    if isdir(args.wave) and exists(args.text):
        script_dict = process_script(args.text)
        wave_dict = process_wave(args.wave)
    else:
        parser.print_help()

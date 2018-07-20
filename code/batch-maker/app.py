#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''Match valid script ID and wave files to create batches to upload.'''

import argparse
import codecs
from os import mkdir, walk
from os.path import exists, getsize, isdir, isfile, join, splitext
from zipfile import ZIP_DEFLATED, ZipFile

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


def save_zip_script(filename, id_list, wave_dict, script_dict):
    script_file = open(filename+'.txt', 'w', encoding='utf-8')
    zip_file = ZipFile(filename+'.zip', 'w', compression=ZIP_DEFLATED)
    for i in id_list:
        script_file.writelines(i+'\t'+script_dict[i])
        zip_file.write(wave_dict[i], arcname=i+'.wav')
    script_file.close()
    zip_file.close()

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
    parser.add_argument('--zipdir',
                        default='zippeddata',
                        help='Directory to save zipped data.')
    parser.add_argument('--limit',
                        default=200,
                        help='Limit size of zip files, default to 200.')

    args = parser.parse_args()
    parser.print_help()

    if isdir(args.wave) and exists(args.text) and not exists(args.zipdir):
        script_dict = process_script(args.text)
        wave_dict = process_wave(args.wave)
        valid_id = sorted([i for i in script_dict.keys() if i in wave_dict.keys()])
        max_size = args.limit * 1024 * 1024
        id_start = ''
        id_end = ''
        accumulated_size = 0
        id_list = []
        if valid_id:
            mkdir(args.zipdir)
        for i in valid_id:
            if not id_start:
                id_start = i
            if not id_end:
                id_end = i
            cur_size = getsize(wave_dict[i])
            if accumulated_size + cur_size > max_size:
                save_zip_script(join(args.zipdir, id_start+'-'+id_end), id_list, wave_dict, script_dict)
                id_start = i
                id_end = i
                accumulated_size = cur_size
                id_list.clear()
                id_list.append(i)
            else:
                id_end = i
                accumulated_size = accumulated_size + cur_size
                id_list.append(i)
        if id_list:
            save_zip_script(join(args.zipdir, id_start+'-'+id_end), id_list, wave_dict, script_dict)

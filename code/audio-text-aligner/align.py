#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''This module aligns audio and text'''

import codecs

import chardet
from aeneas.executetask import ExecuteTask
from aeneas.task import Task


def process_files(text_file, audio_file):
    '''Process files'''
    text = open(text_file, 'rb').read()
    try:
        encoding = chardet.detect(text)['encoding']
        text = codecs.open(text_file, 'rb', encoding=encoding).read()
    except UnicodeDecodeError:
        text = codecs.open(text_file, 'rb', encoding='gbk').read()
    finally:
        with codecs.open(text_file, 'wb', encoding='utf-8') as f:
            f.write(text)

    config_string = 'task_language=ita|is_text_type=plain|os_task_file_format=json'
    task = Task(config_string=config_string)
    task.audio_file_path_absolute = audio_file
    task.text_file_path_absolute = text_file
    task.sync_map_file_path_absolute = audio_file + '.json'
    ExecuteTask(task).execute()
    task.output_sync_map_file()
    return audio_file + '.json'

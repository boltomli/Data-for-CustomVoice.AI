#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''This module aligns audio and text'''

import codecs
from os import linesep

import chardet
import jieba
from aeneas.executetask import ExecuteTask
from aeneas.task import Task
from nltk.tokenize import sent_tokenize
from nltk.tokenize.punkt import PunktLanguageVars, PunktSentenceTokenizer

import utils


class ChineseLanguageVars(PunktLanguageVars):
    sent_end_chars = ('。', '！', '？', '”')


def process_files(text_file, audio_file, lang):
    '''Process files'''
    text = open(text_file, 'rb').read()
    try:
        encoding = chardet.detect(text)['encoding']
        text = codecs.open(text_file, 'rb', encoding=encoding).read()
    except UnicodeDecodeError:
        text = codecs.open(text_file, 'rb', encoding='gbk').read()
    finally:
        text = text.replace('\r', ' ').replace('\n', ' ')
        if (lang.lower() == 'zho'):
            tokenizer = PunktSentenceTokenizer(lang_vars=ChineseLanguageVars)
            sentences = tokenizer.tokenize(' '.join(jieba.cut(text)))
        else:
            try:
                sentences = sent_tokenize(text, utils.allowed_languages()[lang])
            except LookupError:
                sentences = sent_tokenize(text)
        with codecs.open(text_file, 'wb', encoding='utf-8') as f:
            f.write(linesep.join(sentences))

    config_string = 'task_language='+lang+'|is_text_type=plain|os_task_file_format=json'
    task = Task(config_string=config_string)
    task.audio_file_path_absolute = audio_file
    task.text_file_path_absolute = text_file
    task.sync_map_file_path_absolute = audio_file + '.json'
    ExecuteTask(task).execute()
    task.output_sync_map_file()
    return audio_file + '.json'

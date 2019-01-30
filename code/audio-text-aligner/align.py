#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''This module aligns audio and text'''

import codecs
import json
import re
import tempfile
from os import linesep
from os.path import join
from zipfile import ZIP_DEFLATED, ZipFile

import chardet
import jieba
from aeneas.executetask import ExecuteTask
from aeneas.task import Task
from nltk.tokenize import sent_tokenize
from nltk.tokenize.punkt import PunktLanguageVars, PunktSentenceTokenizer
from pydub import AudioSegment

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
    ExecuteTask(task).execute()
    result = json.loads(task.sync_map.json_string)
    with open(audio_file+'.txt', 'wb') as f:
        f.write(codecs.BOM_UTF16_LE)
    with tempfile.TemporaryDirectory() as temp_dir:
        for fragment in result['fragments']:
            file_id = re.sub(r'\D', '', fragment['id'])
            if (file_id):
                segment_audio(audio_file, float(fragment['begin']), float(fragment['end']), join(temp_dir, file_id))
                append_zip(join(temp_dir, file_id), file_id, audio_file+'.zip')
                append_txt(fragment['lines'], file_id, audio_file+'.txt')
    with ZipFile(audio_file+'.audiozip_script.zip', 'w', compression=ZIP_DEFLATED) as f:
        f.write(audio_file+'.zip', arcname='audio.zip')
        f.write(audio_file+'.txt', arcname='script.txt')
    return audio_file+'.audiozip_script.zip'


def segment_audio(in_audio_file, time_begin, time_end, out_audio_file):
    time_begin = time_begin * 1000
    time_end = time_end * 1000
    newAudio = AudioSegment.from_file(in_audio_file)
    newAudio = newAudio[time_begin:time_end]
    newAudio.export(out_audio_file, format="wav")


def append_zip(in_audio_file, file_id, out_zip_file):
    with ZipFile(out_zip_file, 'a', compression=ZIP_DEFLATED) as f:
        f.write(in_audio_file, arcname=file_id+'.wav')


def append_txt(text, file_id, out_txt_file):
    with open(out_txt_file, 'ab') as f:
        f.write((file_id+'\t'+' '.join(text)+'\n').encode('utf-16-le'))

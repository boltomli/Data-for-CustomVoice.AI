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
from aeneas.runtimeconfiguration import RuntimeConfiguration
from aeneas.task import Task
from nltk.tokenize import sent_tokenize
from nltk.tokenize.punkt import PunktLanguageVars, PunktSentenceTokenizer
from pydub import AudioSegment

import utils


class ChineseLanguageVars(PunktLanguageVars):
    sent_end_chars = ('。', '！', '？', '”')


def cut_sent(para):
    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    para = para.rstrip()
    return para.split("\n")


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
        if lang.lower() == 'zho' or lang.lower() == 'cmn':
            tokenizer = PunktSentenceTokenizer(lang_vars=ChineseLanguageVars)
            sentences = tokenizer.tokenize(' '.join(jieba.cut(text)))
        elif lang.lower() == 'jpn':
            sentences = cut_sent(text)
        else:
            try:
                sentences = sent_tokenize(text, utils.allowed_languages()[lang])
            except LookupError or TypeError:
                sentences = sent_tokenize(text)
        with codecs.open(text_file, 'wb', encoding='utf-8') as f:
            f.write(linesep.join(sentences))

    config_string = '|'.join(['task_language='+lang, 'is_text_type=plain', 'os_task_file_format=json'])
    task = Task(config_string=config_string)
    task.audio_file_path_absolute = audio_file
    task.text_file_path_absolute = text_file
    rconf = task.rconf
    if lang.lower() == 'jpn':
        rconf[RuntimeConfiguration.TTS] = 'macos'
    ExecuteTask(task, rconf).execute()
    result = json.loads(task.sync_map.json_string)
    with open(audio_file+'.txt', 'wb') as f:
        f.write(codecs.BOM_UTF16_LE)
    with tempfile.TemporaryDirectory() as temp_dir:
        with ZipFile(audio_file+'.zip', 'w', compression=ZIP_DEFLATED) as f:
            for fragment in result['fragments']:
                file_id = re.sub(r'\D', '', fragment['id'])
                if (file_id):
                    segment_audio(audio_file, float(fragment['begin']), float(fragment['end']), join(temp_dir, file_id))
                    f.write(join(temp_dir, file_id), arcname=file_id+'.wav')
                    append_txt(fragment['lines'], file_id, audio_file+'.txt')
    with ZipFile(audio_file+'.audio_script.zip', 'w', compression=ZIP_DEFLATED) as f:
        f.write(audio_file+'.zip', arcname='audio.zip')
        f.write(audio_file+'.txt', arcname='script.txt')
    result['splitzip'] = audio_file+'.audio_script.zip'
    return result


def segment_audio(in_audio_file, time_begin, time_end, out_audio_file):
    time_begin = time_begin * 1000
    time_end = time_end * 1000
    newAudio = AudioSegment.from_file(in_audio_file)
    newAudio = newAudio[time_begin:time_end]
    newAudio.export(out_audio_file, format="wav")


def append_txt(text, file_id, out_txt_file):
    with open(out_txt_file, 'ab') as f:
        f.write((file_id+'\t'+' '.join(text)+'\n').encode('utf-16-le'))

#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''This module provides parsers'''

from flask_restplus import reqparse
from werkzeug.datastructures import FileStorage

UPLOAD_FILES = reqparse.RequestParser()
UPLOAD_FILES.add_argument('text_file',
                          location='files',
                          required=True,
                          type=FileStorage,
                          help='Text file')
UPLOAD_FILES.add_argument('audio_file',
                          location='files',
                          required=True,
                          type=FileStorage,
                          help='Audio file')
UPLOAD_FILES.add_argument('lang',
                          location='form',
                          required=True,
                          default='eng',
                          help='Language (see langs endpoint for available values')

DOWNLOAD_FILES = reqparse.RequestParser()
DOWNLOAD_FILES.add_argument('zip_file',
                          location='form',
                          required=True,
                          help='Zip file path (from upload)')

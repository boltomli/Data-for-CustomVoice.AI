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

#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''This is the server module for the app'''

import os

import magic
from flask import Flask, send_file
from flask_restplus import Api, Resource
from flask_uploads import (EXECUTABLES, SCRIPTS, AllExcept, UploadSet,
                           configure_uploads, patch_request_class)

import align
import parsers

# Settings
DEBUG = False
STATIC_PATH = 'static'
UPLOADS_DEFAULT_DEST = '/'.join([STATIC_PATH, 'upload'])
UPLOADS_DEFAULT_URL = UPLOADS_DEFAULT_DEST

# Application, RESTful API and namespace
APP = Flask(__name__, static_folder=STATIC_PATH)
APP.config.from_object(__name__)
API = Api(APP, version='1.0', title='Audio forced alignment with text API', doc='/',
          description='Forced align audio with text (line by line).')
NS = API.namespace('align')

# Uploads

UPLOADED_ATTEMPTS = UploadSet('attempts', AllExcept(SCRIPTS + EXECUTABLES))
configure_uploads(APP, UPLOADED_ATTEMPTS)
patch_request_class(APP, 100 * 1024 * 1024) # 100M file size limit

# APIs
@NS.route('/upload/')
class UploadAndAlign(Resource):
    @API.expect(parsers.UPLOAD_FILES)
    def post(self):
        '''Align audio and text from uploading'''
        args = parsers.UPLOAD_FILES.parse_args()
        text_file = UPLOADED_ATTEMPTS.save(args['text_file'])
        audio_file = UPLOADED_ATTEMPTS.save(args['audio_file'])
        json_file = align.process_files(UPLOADED_ATTEMPTS.path(text_file), UPLOADED_ATTEMPTS.path(audio_file))
        mime = magic.from_file(json_file, mime=True)
        return send_file(json_file, mimetype=mime)

if __name__ == '__main__':
    APP.run(host='0.0.0.0')

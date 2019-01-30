#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''This is the server module for the app'''

import os

import magic
from flask import Flask, send_file
from flask_restplus import Api, Resource, errors
from flask_uploads import (AUDIO, TEXT, UploadSet, configure_uploads,
                           patch_request_class)

import align
import parsers
import utils

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

UPLOADED_ATTEMPTS = UploadSet('attempts', AUDIO + TEXT)
configure_uploads(APP, UPLOADED_ATTEMPTS)
patch_request_class(APP, 100 * 1024 * 1024) # 100M file size limit

# APIs
@NS.route('/upload/')
class UploadAndAlign(Resource):
    @API.expect(parsers.UPLOAD_FILES)
    def post(self):
        '''Align audio and text from uploading'''
        if not utils.download_punkt():
            errors.abort(code=500, message='Cannot download NLTK punkt data properly')
        args = parsers.UPLOAD_FILES.parse_args()
        if args['lang'] not in utils.allowed_languages().keys():
            errors.abort(code=500, message='Language is not supported yet, try eng, ita, zho, etc.')
        text_file = UPLOADED_ATTEMPTS.save(args['text_file'])
        audio_file = UPLOADED_ATTEMPTS.save(args['audio_file'])
        result_file = align.process_files(UPLOADED_ATTEMPTS.path(text_file), UPLOADED_ATTEMPTS.path(audio_file), args['lang'])
        mime = magic.from_file(result_file, mime=True)
        return send_file(result_file, mimetype=mime)

@NS.route('/langs/')
class AllowedLanguages(Resource):
    def get(self):
        '''Get allowed languages'''
        return utils.allowed_languages()

if __name__ == '__main__':
    APP.run(host='0.0.0.0')

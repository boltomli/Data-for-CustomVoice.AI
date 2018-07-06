#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''This is the server module for the app'''

import os
from flask import Flask, send_file
from flask_restplus import Api, Resource
from flask_uploads import UploadSet, configure_uploads, patch_request_class, AllExcept, SCRIPTS, EXECUTABLES
from werkzeug.utils import secure_filename
import magic
import parsers, conv

# Settings
DEBUG = False
STATIC_PATH = 'static'
UPLOADS_DEFAULT_DEST = '/'.join([STATIC_PATH, 'upload'])
UPLOADS_DEFAULT_URL = UPLOADS_DEFAULT_DEST

# Application, RESTful API and namespace
APP = Flask(__name__, static_folder=STATIC_PATH)
APP.config.from_object(__name__)
API = Api(APP, version='1.0', title='Text encoding converter API', doc='/api',
          description='Convert text encoding if not well supported.')
NS = API.namespace('conv')

# Uploads

UPLOADED_ATTEMPTS = UploadSet('attempts', AllExcept(SCRIPTS + EXECUTABLES))
configure_uploads(APP, UPLOADED_ATTEMPTS)
patch_request_class(APP, 5 * 1024 * 1024) # 5M file size limit

# APIs
@NS.route('/retrieve/')
class RetrieveAndConvert(Resource):
    @API.expect(parsers.TEXT_URL)
    def post(self):
        '''Get text from URL and convert if necessary'''
        args = parsers.TEXT_URL.parse_args()
        url = args['url']
        filename = secure_filename(url)
        return conv.process_url(url, filename)

@NS.route('/upload/')
class UploadAndConvert(Resource):
    @API.expect(parsers.UPLOAD_FILE)
    def post(self):
        '''Convert text from uploading if necessary'''
        args = parsers.UPLOAD_FILE.parse_args()
        uploaded_file = args['file']
        filename = UPLOADED_ATTEMPTS.save(uploaded_file)
        return conv.process_file(UPLOADED_ATTEMPTS.path(filename))

@NS.route('/view/<string:filename>')
class ViewFile(Resource):
    def get(self, filename):
        '''View a file'''
        filepath = os.path.abspath(UPLOADED_ATTEMPTS.path(filename))
        mime = magic.from_file(filepath, mime=True)
        return send_file(filepath, mimetype=mime)

if __name__ == '__main__':
    APP.run(host='0.0.0.0')

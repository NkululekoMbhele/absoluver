# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Endpoints sample application.

Demonstrates how to create a simple echo API as well as how to deal with
various authentication methods.
"""

import base64
import json
import logging

from flask import Flask, jsonify, request

from flask_cors import cross_origin


app = Flask(__name__)



@app.route('/echo', methods=['POST'])
def echo():
    """Simple echo service."""
    message = request.get_json().get('message', '')
    return jsonify({'message': message})


@app.route('/', methods=['POST', 'GET'])
def echo():
    """Simple echo service."""
    return jsonify({'message': "Hello World!"})



if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

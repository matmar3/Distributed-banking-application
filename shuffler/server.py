# coding=utf-8
import os
import json
from random import shuffle
from flask import Flask, jsonify, request, make_response
from flasgger import Swagger, swag_from
from flask_api import status    # HTTP Status Codes
from werkzeug import exceptions as ex
from models import Response, UBRList, Endpoint
import requests
import logging
from logging.config import fileConfig

# Bank servers
endpoints = [
    Endpoint('10.0.1.12', 8080, '/requests/process'),
    Endpoint('10.0.1.13', 8080, '/requests/process'),
    Endpoint('10.0.1.14', 8080, '/requests/process'),
    Endpoint('10.0.1.15', 8080, '/requests/process'),
]

# Pull options from environment
debug = (os.getenv('DEBUG', 'False') == 'True')
port = os.getenv('PORT', '8080')

# Initialize Flask
app = Flask(__name__)

# Configure logging
fileConfig('/vagrant/shuffler/logger.cfg')
log = logging.getLogger()

# Configure Swagger before initializing it
app.config['SWAGGER'] = {
    "specs": [
        {
            "endpoint": 'spec',
            "route": '/spec'
        }
    ],
    "specs_route": "/apidocs/"
}

template = {
    "swagger": "2.0",
    "info": {
        "description": "Semestrální práce z předmětu DS",
        "version": "1.0.0",
        "title": "Distribuovaná bankovní aplikace - Shuffler",
        "contact": {
          "email": "martinm@students.zcu.cz"
        },
        "license": {
          "name": "Apache 2.0",
          "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
        }
    }
}

# Initialize Swagger after configuring it
Swagger(app, template=template)

######################################################################
# ERROR Handling
######################################################################
@app.errorhandler(ex.HTTPException)
def handle_generic_error(e):
    response = Response(code=e.code, description=e.description)
    return make_response(response.serialize(), e.code)


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, ex.HTTPException):
        return handle_generic_error(e)

    # pass through Value errors
    if isinstance(e, ValueError):
        return handle_generic_error(ex.BadRequest(e.message))

    # handling non-HTTP exceptions only
    return handle_generic_error(ex.InternalServerError)

######################################################################
#  Index
######################################################################
@app.route("/")
def index():
    return make_response(
        jsonify(
            name='Distribuovaná bankovní aplikace - Shuffler',
            version='1.0.0',
            docs=request.base_url + 'apidocs/'
        ), status.HTTP_200_OK
    )


######################################################################
#  API Requests
######################################################################
@app.route("/requests/shuffle", methods=['POST'])
@swag_from("api/shuffle.yml")
def shuffle_requests():
    global endpoints

    # process request data
    ubr_list = UBRList()
    ubr_list.deserialize(request.get_json())
    valid_json_data = ubr_list.serialize()

    # init results
    success = []
    fail = []

    app.logger.info('Sending data to all endpoints.')
    # shuffle endpoints
    shuffle(endpoints)
    for endpoint in endpoints:
        # shuffle data
        shuffle(valid_json_data)
        # sent data
        url = "http://{0}:{1}{2}".format(endpoint.host, endpoint.port, endpoint.route)
        try:
            status_code = requests.post(url, json=valid_json_data).status_code
        except requests.exceptions.RequestException:
            status_code = status.HTTP_408_REQUEST_TIMEOUT
        # handle response
        if status_code is status.HTTP_200_OK:
            success.append({'endpoint': url, 'code': status_code})
        else:
            fail.append({'endpoint': url, 'code': status_code})
    app.logger.debug('\n' + json.dumps({'successful': success, 'failed': fail}, indent=4, sort_keys=True))

    # response
    if len(fail) == 0:
        response = Response(
            code=status.HTTP_200_OK,
            description='Bankovní operace úspěšně zpracovány'
        )
        return make_response(response.serialize(), status.HTTP_200_OK)
    else:
        response = Response(
            code=status.HTTP_503_SERVICE_UNAVAILABLE,
            description='Nepodařilo se zpracovat bankovní oprace'
        )
        return make_response(response.serialize(), status.HTTP_503_SERVICE_UNAVAILABLE)


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port), debug=debug, threaded=True)

# coding=utf-8
import os
import time
from flask import Flask, jsonify, request, make_response
from flasgger import Swagger, swag_from
from flask_api import status    # HTTP Status Codes
from werkzeug import exceptions as ex
from models import BankRequest, UniqueBankRequest, Response, UBRList
import requests
import logging

# Shuffler IP
forward_host = '10.0.1.11'
forward_port = 8080
forward_route = '/shuffle'

# Server timer
last_request = time.time()
interval = 10  # 60  # 1 minute

# Temporary stored requests
counter = 1
stored_requests = UBRList()

# Pull options from environment
debug = (os.getenv('DEBUG', 'False') == 'True')
port = os.getenv('PORT', '8080')

# Initialize Flask
app = Flask(__name__)

# Configure root path
app.config['APPLICATION_ROOT'] = '/v1'

# Configure logging
app.logger.setLevel(logging.INFO)

# Configure Swagger before initializing it
app.config['SWAGGER'] = {
    "specs": [
        {
            "endpoint": 'v1_spec',
            "route": '/v1/spec'
        }
    ],
    "specs_route": "/v1/apidocs/"
}

template = {
    "swagger": "2.0",
    "info": {
        "description": "Semestrální práce z předmětu DS",
        "version": "1.0.0",
        "title": "Distribuovaná bankovní aplikace - Sequencer",
        "contact": {
          "email": "martinm@students.zcu.cz"
        },
        "license": {
          "name": "Apache 2.0",
          "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
        }
    },
    "basePath": "/v1"
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
        return e

    # handling non-HTTP exceptions only
    return handle_generic_error(ex.InternalServerError)

######################################################################
#  Index
######################################################################
@app.route("/")
def index():
    return make_response(
        jsonify(
            name='Distribuovaná bankovní aplikace - Sequencer',
            version='1.0.0',
            docs=request.base_url + 'v1/apidocs/'
        ), status.HTTP_200_OK
    )


######################################################################
#  API Request
######################################################################
@app.route("/request", methods=['POST'])
@swag_from("api/request.yml")
def bank_request():
    global stored_requests
    global last_request
    global interval
    global counter
    global forward_host
    global forward_port
    global forward_route

    # process request data
    req = BankRequest()
    req.deserialize(request.get_json())
    # creates new bank request
    unique_req = UniqueBankRequest()
    unique_req.__setattr__('id', counter)
    unique_req.__setattr__('amount', req.amount)
    unique_req.__setattr__('operation', req.operation)
    # add request to queue
    stored_requests.add(unique_req)
    counter += 1

    # compute interval between requests
    actual_time = time.time()
    diff = actual_time - last_request
    app.logger.info('%d sec diff', diff)

    # check interval
    if diff > interval and stored_requests.size() > 0:
        # sent data
        url = "http://{0}:{1}{2}".format(forward_host, forward_port, forward_route)
        app.logger.info('Posting data to %s in count of %d requests.', url, stored_requests.size())
        try:
            status_code = requests.post(
                url,
                json=stored_requests.serialize()
            ).status_code
        except requests.exceptions.RequestException:
            status_code = status.HTTP_408_REQUEST_TIMEOUT
        # handle response
        if status_code is status.HTTP_200_OK:
            last_request = actual_time
            stored_requests.clean()
        else:
            app.logger.error('POST to %s failed with status code %d.', url, status_code)

    return make_response(unique_req.serialize(), status.HTTP_200_OK)


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port), debug=debug)

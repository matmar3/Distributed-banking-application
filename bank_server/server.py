# coding=utf-8
import os
from flask import Flask, jsonify, request, make_response
from flasgger import Swagger, swag_from
from flask_api import status    # HTTP Status Codes
from werkzeug import exceptions as ex
from models import Response, UBRList, Account
import logging
from logging.config import fileConfig

# Local account
account = Account()
last_processed_request_id = 0

# Pull options from environment
debug = (os.getenv('DEBUG', 'False') == 'True')
port = os.getenv('PORT', '8080')

# Initialize Flask
app = Flask(__name__)

# Configure root path
app.config['APPLICATION_ROOT'] = '/v1'

# Configure logging
fileConfig('/vagrant/bank_server/logger.cfg')
log = logging.getLogger()

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
        "title": "Distribuovaná bankovní aplikace - BankServer",
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
            name='Distribuovaná bankovní aplikace - BankServer',
            version='1.0.0',
            docs=request.base_url + 'v1/apidocs/'
        ), status.HTTP_200_OK
    )


######################################################################
#  API Account
######################################################################
@app.route("/account", methods=['GET'])
@swag_from("api/account.yml")
def account_details():
    global account

    app.logger.info('Retrieving account data.')
    return make_response(account.serialize(), status.HTTP_200_OK)


######################################################################
#  API Requests
######################################################################
@app.route("/requests/process", methods=['POST'])
@swag_from("api/requests.yml")
def process_requests():
    global account
    global last_processed_request_id

    # process request data
    ubr_list = UBRList()
    ubr_list.deserialize(request.get_json())

    app.logger.debug('Processing received bank requests.')

    # sort request data
    sorted_bank_requests = ubr_list.get_sorted()

    # perform bank requests in order
    for req in sorted_bank_requests:
        if last_processed_request_id < req.id:
            if req.operation == 'CREDIT':
                account.increase_balance(req.amount)
            else:
                account.decrease_balance(req.amount)
            last_processed_request_id = req.id

    # response
    response = Response(
        code=status.HTTP_200_OK,
        description='Bankovní operace úspěšně zpracovány.'
    )
    return make_response(response.serialize(), status.HTTP_200_OK)


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port), debug=debug)

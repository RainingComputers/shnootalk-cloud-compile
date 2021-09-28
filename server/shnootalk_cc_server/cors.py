from typing import Any

from flask import Flask
from flask import Response
from flask import request
from flask import make_response


def cors_options_response() -> Any:
    if request.method != 'OPTIONS':
        return None

    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response


def cors_after_request(response: Response) -> Response:
    if 'Access-Control-Allow-Origin' in response.headers:
        return response

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def cors(app: Flask) -> None:
    app.before_request(cors_options_response)
    app.after_request(cors_after_request)

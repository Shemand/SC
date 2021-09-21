from flask import g, request

from ...sc_common.authenticate import read_token
from ..MiddlewareResponse import MiddlewareResponse


def attach_before_request(app):
    @app.before_request
    def before_req():
        g.middleware = MiddlewareResponse(request.headers, request.json)

from flask import Blueprint, g

from backend.src.sc_http.handlers.LogsHandlers import get_updating_logs_handler

mod = Blueprint('Logs', __name__, url_prefix='/logs/')


@mod.route('/update', methods=['GET'])
def get_updating_logs():
    middleware = g.middleware
    return get_updating_logs_handler(middleware)

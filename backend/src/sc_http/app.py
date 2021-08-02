from flask import Blueprint

from .flask.CommonsRoutes import mod as common_mod
from .flask.ComputersRoutes import mod as computers_mod
from .flask.CryptoGatewaysRoutes import mod as crypto_gateways_mod
from .flask.DevicesRoutes import mod as devices_mod
from .flask.LogsRoutes import mod as logs_mod
from .flask.StatisticsRoutes import mod as statistics_mod
from .flask.UpdatesRoutes import mod as updates_mod
from .flask.UsersRoutes import mod as users_mod
from .flask.before_request import attach_before_request


def initialize_flask_routes(app):
    attach_before_request(app)
    app.register_blueprint(common_mod)
    app.register_blueprint(computers_mod)
    app.register_blueprint(crypto_gateways_mod)
    app.register_blueprint(devices_mod)
    app.register_blueprint(logs_mod)
    app.register_blueprint(statistics_mod)
    app.register_blueprint(updates_mod)
    app.register_blueprint(users_mod)
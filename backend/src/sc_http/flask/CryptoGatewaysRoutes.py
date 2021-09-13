from flask import Blueprint, g

from ..handlers.CryptoGatewaysHandlers import get_crypto_gateways_handler

mod = Blueprint('CryptoGateways', __name__, url_prefix='/crypto_gateways')


def attach_crypto_gateway_routes(mod):
    @mod.route('/available', methods=['GET'])
    def get_crypto_gateways():
        middleware = g.middleware
        return get_crypto_gateways_handler(middleware)

from .BlueprintAttacher import BlueprintAttacher


class CryptoGatewaysRoutes(BlueprintAttacher):
    def __init__(self, mod, base_name):
        super().__init__(mod, base_name)

    def _attach(self, route):
        @route('/', methods=['GET'])
        def get_crypto_gateways(res):
            '''Get crypto gateways of distict'''
            return '{}'

        @route('/<crypto_gateway>/ip', methods=['GET'])
        def get_crypto_gateway_ip(res):
            '''Get all ip belongs to crypto gateway'''
            return '{}'

from .BlueprintAttacher import BlueprintAttacher


def attach_crypto_gateway_routes(mod):
    @mod.route('/<district_name>/crypto_gateways/available', methods=['GET'])
    def get_crypto_gateways():
        '''Get crypto gateways of distict'''
        return '{}'

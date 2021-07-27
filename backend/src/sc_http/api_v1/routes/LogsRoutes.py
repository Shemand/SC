from .BlueprintAttacher import BlueprintAttacher


def attach_log_routes(mod):
    @mod.route('/<district_name>/logs/update', methods=['GET'])
    def get_updating_logs(district_name):
        '''Function for getting logs about updates'''
        return '{}'

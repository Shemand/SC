from .BlueprintAttacher import BlueprintAttacher


class LogsRoutes(BlueprintAttacher):
    def __init__(self, mod, base_name):
        super().__init__(mod, base_name)

    def _attach(self, route):
        @route('/update', methods=['GET'])
        def get_updating_logs(res):
            res = self.make_response()
            '''Function for getting logs about updates'''
            return '{}'

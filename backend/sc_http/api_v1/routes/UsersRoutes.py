from .BlueprintAttacher import BlueprintAttacher


class UsersRoutes(BlueprintAttacher):
    def __init__(self, mod, base_name):
        super().__init__(mod, base_name)

    def _attach(self, route):
        @route('/role', methods=['GET'])
        def get_user_role(res):
            '''Function for getting information about computers in districts according'''
            return '{}'

        @route('/auth', methods=['GET'])
        def authenticate(res):
            return '{}'

        @route('/registration', methods=['POST'])
        def registration(res):
            return '{}'

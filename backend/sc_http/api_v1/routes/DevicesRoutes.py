from .BlueprintAttacher import BlueprintAttacher


class DevicesRoutes(BlueprintAttacher):
    def __init__(self, mod, base_name):
        super().__init__(mod, base_name)

    def _attach(self, route):
        @route('/', methods=['GET'])
        def get_devices(district_name):
            '''Function for getting devices according user privileges'''
            return '{}'

        @route('/add', methods=['PUT'])
        def add_device(res):
            '''Function for add new device.

            User can create device only according with him privileges and container.

            '''
            return '{}'

        @route('/remove/<device_id>', methods=['DELETE'])
        def remove_device(res):
            '''Function for removing device.

            User can see only devices according with him container.

            '''
            return '{}'

        @route('/<device_id>/comment', methods=['PUT'])
        def set_device_comment(res):
            '''Function for changing comment of device.'''
            return '{}'

        @route('/<device_name>/type/<type>', methods=['PUT'])
        def change_device_type(res):
            '''Function for changing type of device(ARM, Server)'''
            return '{}'

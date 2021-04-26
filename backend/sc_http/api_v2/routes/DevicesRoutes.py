from .BlueprintAttacher import BlueprintAttacher


def attach_device_routes(mod):
    @mod.route('/<district_name>/devices', methods=['GET'])
    def get_devices(district_name):
        '''Function for getting devices according user privileges'''
        return '{}'

    @mod.route('/<district_name>/devices/add', methods=['PUT'])
    def add_device(district_name):
        '''Function for add new device.

        User can create device only according with him privileges and container.

        '''
        return '{}'

    @mod.route('/<district_name>/devices/remove/<device_id>', methods=['DELETE'])
    def remove_device(district_name, device_id):
        '''Function for removing device.

        User can see only devices according with him container.

        '''
        return '{}'

    @mod.route('/<district_name>/devices/<device_id>/comment', methods=['PUT'])
    def set_device_comment(district_name, device_id):
        '''Function for changing comment of device.'''
        return '{}'

    @mod.route('/<district_name>/devices/<device_name>/type/<type>', methods=['PUT'])
    def change_device_type(district_name, device_name, type):
        '''Function for changing type of device(ARM, Server)'''
        return '{}'

def get_devices_handler(middleware):
    '''Function for getting devices according user privileges'''
    return '{}'


def add_device_handler(middleware):
    '''Function for add new device.

    User can create device only according with him privileges and container.

    '''
    return '{}'


def remove_device_handler(middleware, device_id):
    '''Function for removing device.

    User can see only devices according with him container.

    '''
    return '{}'


def set_device_comment_handler(middleware, device_id):
    '''Function for changing comment of device.'''
    return '{}'


def change_device_type_handler(middleware, device_name, type):
    '''Function for changing type of device(ARM, Server)'''
    return '{}'

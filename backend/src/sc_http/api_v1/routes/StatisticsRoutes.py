from .BlueprintAttacher import BlueprintAttacher


def attach_statistic_routes(mod):
    @mod.route('/<district_name>/statistic/', methods=['GET'])
    def get_statistics(district_name):
        '''Function for getting information about computers in districts according'''
        return '{}'

    @mod.route('/<district_name>/statistic', methods=['PUT'])
    def update_statistics(district_name):
        '''Function for updating information about all units of disticts'''
        return '{}'

    @mod.route('/<district_name>/statistic/<statistic_id>', methods=['GET'])
    def get_statistics_by_id(district_name, statistic_id):
        '''Function for getting information about computers by statistic_id'''
        return '{}'

    @mod.route('/<district_name>/statistic/snapshot', methods=['PUT'])
    def make_snapshot(district_name):
        '''Function for making new snapshot of statistic'''
        return '{}'

    @mod.route('/<district_name>/statistic/snapshots/dates/<limit>', methods=['GET'])
    def get_snapshot_dates(district_name, limit):
        '''Function, who returning dates of snapshots

        :param limit - necessary for limit amount of dates, if limit more than quantity of date, will return all dates

        :returns list of dates of snapshots
        '''
        return '{}'

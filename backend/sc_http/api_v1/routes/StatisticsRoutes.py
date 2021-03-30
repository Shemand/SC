from .BlueprintAttacher import BlueprintAttacher


class StatisticsRoutes(BlueprintAttacher):
    def __init__(self, mod, base_name):
        super().__init__(mod, base_name)

    def _attach(self, route):
        @route('/', methods=['GET'])
        def get_statistics(res):
            '''Function for getting information about computers in districts according'''
            return '{}'

        @route('/', methods=['PUT'])
        def update_statistics(res):
            '''Function for updating information about all units of disticts'''
            return '{}'

        @route('/<statistic_id>', methods=['GET'])
        def get_statistics_by_id(res):
            '''Function for getting information about computers by statistic_id'''
            return '{}'

        @route('/snapshot', methods=['PUT'])
        def make_snapshot(res):
            '''Function for making new snapshot of statistic'''
            return '{}'

        @route('/snapshots/dates/<limit>', methods=['GET'])
        def get_snapshot_dates(res):
            '''Function, who returning dates of snapshots

            :param limit - necessary for limit amount of dates, if limit more than quantity of date, will return amount dates

            :returns list of dates of snapshots
            '''
            return '{}'

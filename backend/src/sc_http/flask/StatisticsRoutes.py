from flask import Blueprint, g
from ..handlers.StatisticsHandlers import make_snapshot_handler, get_snapshot_dates_handler, \
    update_statistics_handler, get_statistics_handler

mod = Blueprint('Statistics', __name__, url_prefix='/statistics/')


@mod.route('/', methods=['GET'])
def get_statistics(district_name):
    middleware = g.middleware
    return get_statistics_handler(middleware)


@mod.route('/', methods=['PUT'])
def update_statistics():
    middleware = g.middleware
    return update_statistics_handler(middleware)


@mod.route('/<statistic_id>', methods=['GET'])
def get_statistics_by_id(district_name, statistic_id):
    middleware = g.middleware
    return get_statistics_by_id(middleware, statistic_id)


@mod.route('/snapshot', methods=['PUT'])
def make_snapshot():
    middleware = g.middleware
    return make_snapshot_handler(middleware)


@mod.route('/snapshots/dates/<limit>', methods=['GET'])
def get_snapshot_dates(limit):
    middleware = g.middleware
    return get_snapshot_dates_handler(middleware, limit)

from flask import Blueprint

from backend.sc_http.api_v1.routes.CommonsRoutes import CommonsRoutes
from backend.sc_http.api_v1.routes.ComputersRoutes import ComputersRoutes
from backend.sc_http.api_v1.routes.CryptoGatewaysRoutes import CryptoGatewaysRoutes
from backend.sc_http.api_v1.routes.DevicesRoutes import DevicesRoutes
from backend.sc_http.api_v1.routes.LogsRoutes import LogsRoutes
from backend.sc_http.api_v1.routes.StatisticsRoutes import StatisticsRoutes
from backend.sc_http.api_v1.routes.UpdatesRoutes import UpdatesRoutes
from backend.sc_http.api_v1.routes.UsersRoutes import UsersRoutes

from backend.sc_http.api_v2.routes.CommonsRoutes import attach_common_routes
from backend.sc_http.api_v2.routes.ComputersRoutes import attach_computer_routes
from backend.sc_http.api_v2.routes.CryptoGatewaysRoutes import attach_crypto_gateway_routes
from backend.sc_http.api_v2.routes.DevicesRoutes import attach_device_routes
from backend.sc_http.api_v2.routes.LogsRoutes import attach_log_routes
from backend.sc_http.api_v2.routes.StatisticsRoutes import attach_statistic_routes
from backend.sc_http.api_v2.routes.UpdatesRoutes import attach_update_routes
from backend.sc_http.api_v2.routes.UsersRoutes import attach_user_rotes
from backend.sc_http.api_v2.routes.before_request import attach_before_request

api_v1_mod = Blueprint('apiv1', __name__, url_prefix='/api/v1/')
api_v2_mod = Blueprint('apiv2', __name__, url_prefix='/api/v2/')

ComputersRoutes(api_v1_mod, 'computers')
CryptoGatewaysRoutes(api_v1_mod, 'crypto_gateways')
DevicesRoutes(api_v1_mod, 'devices')
LogsRoutes(api_v1_mod, 'logs')
StatisticsRoutes(api_v1_mod, 'statistics')
CommonsRoutes(api_v1_mod, 'common')
UsersRoutes(api_v1_mod, 'users')
UpdatesRoutes(api_v1_mod, 'update')

attach_before_request(api_v2_mod, mod_path='/api/v2/')
attach_common_routes(api_v2_mod)
attach_computer_routes(api_v2_mod)
attach_crypto_gateway_routes(api_v2_mod)
attach_device_routes(api_v2_mod)
attach_log_routes(api_v2_mod)
attach_statistic_routes(api_v2_mod)
attach_update_routes(api_v2_mod)
attach_user_rotes(api_v2_mod)

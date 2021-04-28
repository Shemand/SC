from flask import Blueprint

from backend.sc_http.api_v1.routes.CommonsRoutes import attach_common_routes
from backend.sc_http.api_v1.routes.ComputersRoutes import attach_computer_routes
from backend.sc_http.api_v1.routes.CryptoGatewaysRoutes import attach_crypto_gateway_routes
from backend.sc_http.api_v1.routes.DevicesRoutes import attach_device_routes
from backend.sc_http.api_v1.routes.LogsRoutes import attach_log_routes
from backend.sc_http.api_v1.routes.StatisticsRoutes import attach_statistic_routes
from backend.sc_http.api_v1.routes.UpdatesRoutes import attach_update_routes
from backend.sc_http.api_v1.routes.UsersRoutes import attach_user_rotes
from backend.sc_http.api_v1.routes.before_request import attach_before_request

api_v1_mod = Blueprint('apiv1', __name__, url_prefix='/api/v1/')

attach_before_request(api_v1_mod, mod_path='/api/v1/')
attach_common_routes(api_v1_mod)
attach_computer_routes(api_v1_mod)
attach_crypto_gateway_routes(api_v1_mod)
attach_device_routes(api_v1_mod)
attach_log_routes(api_v1_mod)
attach_statistic_routes(api_v1_mod)
attach_update_routes(api_v1_mod)
attach_user_rotes(api_v1_mod)

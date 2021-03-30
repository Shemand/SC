from flask import Blueprint

from backend.sc_http.api_v1.routes.CommonsRoutes import CommonsRoutes
from backend.sc_http.api_v1.routes.ComputersRoutes import ComputersRoutes
from backend.sc_http.api_v1.routes.CryptoGatewaysRoutes import CryptoGatewaysRoutes
from backend.sc_http.api_v1.routes.DevicesRoutes import DevicesRoutes
from backend.sc_http.api_v1.routes.LogsRoutes import LogsRoutes
from backend.sc_http.api_v1.routes.StatisticsRoutes import StatisticsRoutes
from backend.sc_http.api_v1.routes.UsersRoutes import UsersRoutes

api_v1_mod = Blueprint('api', __name__, url_prefix='/api/v1/')

ComputersRoutes(api_v1_mod, 'computers')
CryptoGatewaysRoutes(api_v1_mod, 'crypto_gateways')
DevicesRoutes(api_v1_mod, 'devices')
LogsRoutes(api_v1_mod, 'logs')
StatisticsRoutes(api_v1_mod, 'statistics')
CommonsRoutes(api_v1_mod, 'common')
UsersRoutes(api_v1_mod, 'users')
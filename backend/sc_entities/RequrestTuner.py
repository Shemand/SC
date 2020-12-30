import json

from backend.sc_config.config import config
from backend.sc_entities.District.ServiceManager import ServiceManager

class TunedRequest():
    def __init__(self, user=None, data=None, services=None,
                 unit=None, district=None):
        self._user = user
        self._data = data
        self._services = services
        self._unit = unit
        self._district = district

    @property
    def user(self):
        return self._user

    @property
    def data(self):
        return self._data

    @property
    def services(self):
        return self._services

    @property
    def unit(self):
        return self._unit

    @property
    def district(self):
        return self._district

class RequestTuner():

    districts = config.districts

    def prepare_request(self, session, request):
        t_data = self._prepare_data(request.data)
        if self.is_auth(session):
            t_user = self._prepare_user(session)
            t_unit = None
            t_services = []
            t_district = None
        else:

            t_user = None
            t_unit = None
            t_services = []
            t_district = None

        tune = TunedRequest(user=t_user,
                            data=t_data,
                            unit=t_unit,
                            services=t_services,
                            district=t_district)
        return tune

    def _prepare_data(self, data):
        data = json.loads(data)
        return data

    def _prepare_user(self, session):
        if self.is_auth():
            pass

    def is_auth(self, session):
        if 'user_id' in session:
            return True
        return False
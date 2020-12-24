import json
import os

from backend.sc_entities.District.District import District


class Configuration:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Configuration, cls).__new__(cls)
            cls.instance.reload()
        return cls.instance

    def reload(self):
        file = open(os.path.join("sc_config","config.json"), 'r')
        configuration = json.loads(file.read())
        self.__districts = configuration['districts']
        self.districts = {}
        self.districts_names = []
        for district_name in self.__districts:
            self.districts_names.append(self.districts_names)
            self.districts[district_name] = District(district_name)

        self.kaspersky = {
            "win_agent" : configuration['kaspersky']['win_agent_versions'],
            "win_security" : configuration['kaspersky']['win_security_versions'],
            "linux_agent" : configuration['kaspersky']['linux_agent_versions'],
            "linux_security" : configuration['kaspersky']['linux_security_versions'],
            "right_agent" : configuration['kaspersky']['right_agent_versions'],
            "right_security": configuration['kaspersky']['right_security_versions'],
        }

config = Configuration()

JSON_str = str

from backend.sc_http.BlueprintAttacherAbstract import BlueprintAttacherAbstract
from flask import Blueprint
from sqlalchemy import String

from backend.sc_config.config import JSON_str


class ApiComputersRoutes(BlueprintAttacherAbstract):

    def __init__(self, mod: Blueprint, base_name: String) -> None:
        super().__init__(mod, base_name)

    def attach_to_blueprint(self, mod: Blueprint):

        @mod.route(self.to_path('/'), methods=['GET'])
        def get_computers_info() -> JSON_str:
            return '{}'
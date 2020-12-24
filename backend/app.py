from flask import Flask, render_template

from backend.sc_entities.Computer import ComputerActions
from backend.sc_http.api_blueprints import mod as api_mod
from backend.sc_services.ServiceManager import ServiceManager

from backend.sc_config.config import config

app = Flask(__name__,
            static_folder = "./frontend/static",
            template_folder = "./frontend")

app.register_blueprint(api_mod)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == '__main__':
    sm = ServiceManager()
    database = config.districts['SZO'].database
    x = ComputerActions.get_or_create(database, name='SZO-555-1015')
    app.run(host='0.0.0.0', port=5000)
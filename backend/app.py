from flask import Flask, render_template

from backend.sc_config.url import UrlPaths
from backend.sc_database.actions.ComputerActions import ComputerActions
from backend.sc_entities.District.ServiceManager import ServiceManager
from backend.sc_http.api_blueprints import mod as api_mod

from backend.sc_config.config import config

app = Flask(__name__,
            static_folder = "./frontend/static",
            template_folder = "./frontend")
app.config['SECRET_KEY'] = 'ccb711f092ac8ef1805b5045fab7e8a6189cb97ad04565e21b5fbcfc9e542e42'
app.register_blueprint(api_mod)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == '__main__':
    database = config.districts['SZO'].database
    x = ComputerActions.get_or_create(database, name='SZO-555-1015')
    app.run(host='0.0.0.0', port=5000)
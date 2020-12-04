from flask import Flask, render_template

from backend.sc_http.api_blueprints import mod as api_mod
from backend.sc_services.ServiceManager import ServiceManager

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
    app.run(host='0.0.0.0', port=5000)
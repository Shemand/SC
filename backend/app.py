from datetime import date

from flask.json import JSONEncoder

from flask import Flask, render_template
from src.sc_http.app import api_v1_mod

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return int(obj.timestamp()*1000)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

def create_app():
    app = Flask(__name__,
                static_folder="./frontend/static",
                template_folder="./frontend")
    app.config['SECRET_KEY'] = 'ccb711f092ac8ef1805b5045fab7e8a6189cb97ad04565e21b5fbcfc9e542e42'
    app.register_blueprint(api_v1_mod)
    app.json_encoder = CustomJSONEncoder
    return app


app = create_app()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


if __name__ == '__main__':
    # create_app()
    app.run(host='0.0.0.0', port=7598)

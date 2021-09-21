import os
from datetime import date

from flask.json import JSONEncoder

from flask import Flask
from flask_cors import CORS
from src.sc_http.app import initialize_flask_routes
from dotenv import load_dotenv


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
    CORS(app)
    load_dotenv()
    app.config['SECRET_KEY'] = 'ccb711f092ac8ef1805b5045fab7e8a6189cb97ad04565e21b5fbcfc9e542e42'
    app.json_encoder = CustomJSONEncoder
    initialize_flask_routes(app)
    return app


app = create_app()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return '{"error" : "Not found"}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

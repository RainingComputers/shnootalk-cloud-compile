from flask import Flask
from shnootalk_cc_server.api_v1 import server as api_v1_server
from shnootalk_cc_server.cors import cors


def create_app() -> Flask:
    flask_app = Flask(__name__)
    flask_app.register_blueprint(api_v1_server, url_prefix='/shnootalk/compile/api/v1/')
    cors(flask_app)
    return flask_app


app = create_app()

if __name__ == '__main__':
    app.run()

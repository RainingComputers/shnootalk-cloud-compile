from flask import Flask
from shnootalk_cc_server.api_v1 import server as api_v1_server


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(api_v1_server, url_prefix='/api/v1/')
    return app


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run()

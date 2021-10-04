from flask import Flask
from flask.helpers import make_response
from flask import Response
from shnootalk_cc_server.api_v1 import server as api_v1_server
from shnootalk_cc_server.cors import cors

from shnootalk_cc_server.config import HEARTBEAT_JOB_ENABLE, HEARTBEAT_JOB_INTERVAL
from shnootalk_cc_server.threadloop import ThreadLoop
from shnootalk_cc_server.heartbeat import send_heartbeat


def health() -> Response:
    return make_response('', 200)


def create_app() -> Flask:
    flask_app = Flask(__name__)
    flask_app.register_blueprint(api_v1_server, url_prefix='/shnootalk/compile/api/v1/')
    cors(flask_app)

    flask_app.get('/')(health)
    flask_app.get('/health')(health)

    return flask_app


app = create_app()

if HEARTBEAT_JOB_ENABLE == 'true':
    heartbeat_thread = ThreadLoop(HEARTBEAT_JOB_INTERVAL, send_heartbeat)
    heartbeat_thread.start()

if __name__ == '__main__':
    app.run()

import logging
from flask.logging import default_handler

from shnootalk_cc_server.__main__ import app
import shnootalk_cc_server.heartbeat

root = logging.getLogger()
root.addHandler(default_handler)

import logging
from flask.logging import default_handler
from shnootalk_cc_server.config import HEARTBEAT_JOB_ENABLE, HEARTBEAT_JOB_INTERVAL
from shnootalk_cc_server.threadloop import ThreadLoop
from shnootalk_cc_server.heartbeat import send_heartbeat

from shnootalk_cc_server.__main__ import app

root = logging.getLogger()
root.addHandler(default_handler)

if HEARTBEAT_JOB_ENABLE == 'true':
    heartbeat_thread = ThreadLoop(HEARTBEAT_JOB_INTERVAL, send_heartbeat)
    heartbeat_thread.start()

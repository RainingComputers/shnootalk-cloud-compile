import socket
import time

from shnootalk_cc_server.threadloop import ThreadLoop
from shnootalk_cc_server.template import fill_template
from shnootalk_cc_server.kube_apply import kube_apply
from shnootalk_cc_server.config import HEARTBEAT_JOB_ENABLE, HEARTBEAT_JOB_INTERVAL
from shnootalk_cc_server.config import COMPILE_JOB_NAMESPACE


def gen_heartbeat_id() -> str:
    timestamp_now = int(time.time())
    hostname_trimmed = socket.gethostname().split('-')[-1]
    return f'{hostname_trimmed}-{timestamp_now}'


def heartbeat() -> None:
    program = 'fn main() -> int { println("Hello world") return 0 }'

    job_name = f'heartbeat-{gen_heartbeat_id()}'
    job_definition = fill_template(job_name, {'main.shtk': program})

    kube_apply(job_definition, COMPILE_JOB_NAMESPACE)


if HEARTBEAT_JOB_ENABLE == 'true':
    heartbeat_thread = ThreadLoop(HEARTBEAT_JOB_INTERVAL, heartbeat)
    heartbeat_thread.start()

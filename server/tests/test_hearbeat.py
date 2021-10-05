from unittest.mock import Mock

from pytest import MonkeyPatch

import shnootalk_cc_server.heartbeat
from shnootalk_cc_server.template import fill_template


def time_time_stub() -> float:
    return 1633358581.3923664


def socket_gethostname_stub() -> str:
    return 'test-hostname-v15hn0'


def gen_heartbeat_id_stub() -> str:
    return 'v15hn0-1633358581'


def test_heartbeat_id(monkeypatch: MonkeyPatch) -> None:
    socket_stub = Mock()
    socket_stub.gethostname = socket_gethostname_stub

    time_stub = Mock()
    time_stub.time = time_time_stub

    monkeypatch.setattr(shnootalk_cc_server.heartbeat, 'socket', socket_stub)
    monkeypatch.setattr(shnootalk_cc_server.heartbeat, 'time', time_stub)

    heartbeat_id = shnootalk_cc_server.heartbeat.gen_heartbeat_id()

    assert heartbeat_id == 'v15hn0-1633358581'


def test_heartbeat(monkeypatch: MonkeyPatch) -> None:
    program = {'main.shtk': 'fn main() -> int { println("Hello world") return 0 }'}

    kube_apply_mock = Mock()

    monkeypatch.setattr(shnootalk_cc_server.heartbeat, 'gen_heartbeat_id', gen_heartbeat_id_stub)
    monkeypatch.setattr(shnootalk_cc_server.heartbeat, 'kube_apply', kube_apply_mock)

    shnootalk_cc_server.heartbeat.send_heartbeat()

    kube_apply_mock.assert_called_once()

    assert kube_apply_mock.call_args[0][0] == fill_template('heartbeat-v15hn0-1633358581',
                                                            program, True)

    assert kube_apply_mock.call_args[0][1] == 'compile'

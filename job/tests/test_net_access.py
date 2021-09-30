from shnootalk_cc_job.__main__ import run_subprocess


def test_net_access() -> None:
    timedout, output, exitcode = run_subprocess(['ping', '127.0.0.1'])

    assert timedout is False
    assert output == 'ping: connect: Network is unreachable\n'
    assert exitcode == 2

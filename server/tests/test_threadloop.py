import time
from unittest.mock import Mock

from shnootalk_cc_server.threadloop import ThreadLoop


def test_threadloop() -> None:
    callback = Mock()
    threadloop = ThreadLoop(1, callback)
    threadloop.start()
    time.sleep(2)
    threadloop.stop()

    assert callback.call_count <= 4

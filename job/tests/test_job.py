# pylint: disable=import-outside-toplevel

from typing import Tuple

import pytest

from pymongo.collection import Collection
from bson.objectid import ObjectId


fixtures_dir_list = [
    './tests/fixtures/success',
    './tests/fixtures/compile_fail',
    './tests/fixtures/link_fail',
    './tests/fixtures/mongo_env_leak',
    './tests/fixtures/exec_timeout'
]

expected_outputs_list = [
    'Hello world\nfoobar!\n',

    'MODULE main.shtk\n'
    'ERROR in Line 1 Col 4\n'
    '\n'
    'fn main()\n'
    '   ^\n'
    'Invalid return type for MAIN\n',

    "/usr/bin/ld: main.shtk.o: in function `main':\n"
    "main.shtk:(.text+0x2): undefined reference to `doesNotExist'\n"
    "clang: error: linker command failed with exit code 1 (use -v to see invocation)\n",

    'Haha, nice try :)\n',

    None
]

expected_status_list = [
    'SUCCESS',
    'COMPILE_FAILED',
    'CLANG_LINK_FAILED',
    'SUCCESS',
    'EXEC_TIMEDOUT'
]


@pytest.mark.parametrize("fixture_dir,expected_status,expected_output",
                         zip(fixtures_dir_list, expected_status_list, expected_outputs_list))
def test_main(mongo_connection: Tuple[Collection, str],
              empty_dir: str,
              fixture_dir: str,
              expected_status: str,
              expected_output: str) -> None:

    from shnootalk_cc_job.__main__ import main

    collection = mongo_connection[0]
    mongo_id = mongo_connection[1]

    main(fixture_dir, empty_dir, ObjectId(mongo_id))

    expected_doc = {
        '_id': ObjectId(mongo_id),
        'status': expected_status,
        'output': expected_output
    }

    docs = list(collection.find({}))
    assert len(docs) == 1
    assert docs[0] == expected_doc

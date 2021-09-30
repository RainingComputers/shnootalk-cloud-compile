from typing import Dict
from unittest.mock import Mock

from pytest import LogCaptureFixture
from pytest import MonkeyPatch

from flask.testing import FlaskClient

from pymongo.collection import Collection
from bson.objectid import ObjectId

import shnootalk_cc_server.api_v1
from shnootalk_cc_server.api_v1 import fill_template


def test_dispatch_invalid_json(client: FlaskClient) -> None:
    resp = client.post('/shnootalk/compile/api/v1/dispatch', data='This is not valid json')

    assert resp.status_code == 400

    assert resp.json == {'error': 'Cannot parse request body as JSON'}


def test_dispatch(client: FlaskClient, collection: Collection,
                  test_programs: Dict[str, str], monkeypatch: MonkeyPatch) -> None:
    # Mock kube_apply() function, so we don't need a kubernetes cluster to run this test
    mock = Mock()
    monkeypatch.setattr(shnootalk_cc_server.api_v1, 'kube_apply', mock)

    resp = client.post('/shnootalk/compile/api/v1/dispatch', json=test_programs)

    # Check if response is valid JSON
    json_resp = resp.json
    assert json_resp is not None

    program_id = json_resp['_id']

    # Assert if kube_apply() function was called properly
    mock.assert_called_once()
    assert mock.call_args[0][0] == fill_template(program_id, test_programs)
    assert mock.call_args[0][1] == 'compile'

    # Make sure only one document has been inserted, and assert that document
    docs = list(collection.find({}))
    assert len(docs) == 1

    assert docs[0] == {'_id': ObjectId(json_resp['_id']), 'status': 'SCHEDULED'}


def test_dispatch_kube_apply_ex(client: FlaskClient, test_programs: Dict[str, str],
                                monkeypatch: MonkeyPatch, caplog: LogCaptureFixture) -> None:
    def mock_kube_apply() -> None:
        raise Exception

    monkeypatch.setattr(shnootalk_cc_server.api_v1, 'kube_apply', mock_kube_apply)

    resp = client.post('/shnootalk/compile/api/v1/dispatch', json=test_programs)

    assert resp.status_code == 500
    assert 'Unable to dispatch compile job into Kubernetes' in caplog.record_tuples[-1][-1]


def test_dispatch_mongo_ex(client: FlaskClient, test_programs: Dict[str, str],
                           monkeypatch: MonkeyPatch, caplog: LogCaptureFixture) -> None:
    mock = Mock()
    mock.insert_one.side_effect = Exception
    monkeypatch.setattr(shnootalk_cc_server.api_v1, 'mongo_collection', mock)

    resp = client.post('/shnootalk/compile/api/v1/dispatch', json=test_programs)

    assert resp.status_code == 500
    assert caplog.record_tuples[-1][-1] == 'Unable to insert status into MongoDB'


def test_dispatch_prog_too_big(client: FlaskClient) -> None:
    test_programs = {'file1.shtk': 'c'*32768, 'file2.shtk': 'd'*32768}

    resp = client.post('/shnootalk/compile/api/v1/dispatch', json=test_programs)

    assert resp.status_code == 400
    assert resp.json == {'error': 'Program too big'}

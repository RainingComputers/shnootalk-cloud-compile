from typing import Dict
from unittest.mock import Mock


from flask.testing import FlaskClient

from pymongo.collection import Collection
from bson.objectid import ObjectId
from pytest import MonkeyPatch

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

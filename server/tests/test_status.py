from flask.testing import FlaskClient

from pymongo.collection import Collection

from shnootalk_cc_server.messages import Messages


def test_status_invalid_id(client: FlaskClient) -> None:
    resp = client.get('/shnootalk/compile/api/v1/status/invalidId')

    assert resp.status_code == 400

    assert resp.json == {'error': Messages.INVALID_ID}


def test_status_does_not_exist(client: FlaskClient) -> None:
    resp = client.get('shnootalk/compile/api/v1/status/613c7fcf1cbaaff506b1084c')

    assert resp.status_code == 404

    assert resp.json == {'error': Messages.PROG_NOT_FOUND}


def test_status_success(client: FlaskClient, collection: Collection) -> None:
    test_output = 'Hello world'
    test_status = 'SUCCESS'

    # Insert a test document (faking what the job would insert after completing successfully)
    doc_id = collection.insert_one({'output': test_output, 'status': test_status}).inserted_id
    program_id = str(doc_id)

    # Test the endpoint
    resp = client.get(f'/shnootalk/compile/api/v1/status/{program_id}')

    assert resp.json == {'_id': program_id, 'output': test_output, 'status': test_status}

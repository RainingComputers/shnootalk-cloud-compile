from flask.testing import FlaskClient


def test_health(client: FlaskClient) -> None:
    resp = client.get('/')
    assert resp.status_code == 200

    resp = client.get('/health')
    assert resp.status_code == 200

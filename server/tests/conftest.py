from typing import Dict, List

import pathlib

import yaml

import pytest

from flask.testing import FlaskClient

from pymongo.collection import Collection

from shnootalk_cc_server.__main__ import create_app
from shnootalk_cc_server.config import mongo_collection


@pytest.fixture
def client() -> FlaskClient:
    app = create_app()
    return app.test_client()


@pytest.fixture
def collection() -> Collection:
    mongo_collection.delete_many({})
    return mongo_collection


@pytest.fixture
def test_programs() -> Dict[str, str]:
    test_programs_dict = {}
    test_programs_dict['main.shtk'] = pathlib.Path('./tests/fixtures/main.shtk').read_text()
    test_programs_dict['foobar.shtk'] = pathlib.Path('./tests/fixtures/foobar.shtk').read_text()
    return test_programs_dict


@pytest.fixture
def test_job_template() -> List[Dict[str, str]]:
    with open('./tests/fixtures/job.yml') as yaml_f:
        template = list(yaml.safe_load_all(yaml_f))

    return template

from typing import Dict, List, Any

from bson.objectid import ObjectId
from bson.errors import InvalidId

import yaml

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask.wrappers import Response

from shnootalk_cc_server.kube_apply import kube_apply
from shnootalk_cc_server.config import mongo_collection

server = Blueprint('server', __name__)

CONFIG_MAP = 0
JOB = 1


def fill_template(program_id: str, programs: Dict[str, str]) -> List[Dict[str, Any]]:
    # Loads template file with kubernetes resource definition for a configmap and a job
    # Fills the configmap with program files to execute

    config_map_name = f'config-map-{program_id}'
    job_name = f'compile-job-{program_id}'

    with open('./shnootalk_cc_server/templates/job.yml', encoding='utf8') as yaml_f:
        job_template = list(yaml.safe_load_all(yaml_f))

    job_template[CONFIG_MAP]['metadata']['name'] = config_map_name

    job_template[CONFIG_MAP]['data'] = programs

    job_template[JOB]['metadata']['name'] = job_name

    job_template[JOB]['spec']['template']['spec']['containers'][0]['command'][-1] = program_id

    job_template[JOB]['spec']['template']['spec']['volumes'][0]['configMap']['name'] =\
        config_map_name

    return job_template


@server.post('/dispatch')
def dispatch() -> Response:
    # Get programs to run as a JSON key string pair, key being the file name
    programs = request.get_json()

    if programs is None:
        return make_response("Cannot parse request body as JSON", 400)

    doc_id = mongo_collection.insert_one({'status': 'SCHEDULED'}).inserted_id

    # Create a kubernetes job with files mounted as configmap, and deploy job
    job_definition = fill_template(str(doc_id), programs)

    kube_apply(job_definition)

    # return id so client can poll the status of execution
    return jsonify({'_id': str(doc_id)})


@server.route('/status/<program_id>')
def status(program_id: str) -> Response:
    try:
        object_id = ObjectId(program_id)
    except InvalidId:
        return make_response("Invalid id", 400)

    doc = mongo_collection.find_one({'_id': object_id})

    if doc is None:
        return make_response("Program with this id was not found", 404)

    doc['_id'] = str(doc['_id'])

    return jsonify(doc)

import logging

from bson.objectid import ObjectId
from bson.errors import InvalidId

from flask import Blueprint, Response
from flask import jsonify, make_response, request

from shnootalk_cc_server.kube_apply import kube_apply
from shnootalk_cc_server.config import mongo_collection, COMPILE_JOB_NAMESPACE

from shnootalk_cc_server.template import fill_template
from shnootalk_cc_server.validate import validate

server = Blueprint('server', __name__)
logger = logging.getLogger(__name__)


@server.post('/dispatch')
def dispatch() -> Response:
    # Get programs to run as a JSON key string pair, key being the file name
    programs = request.get_json()

    if programs is None:
        return make_response(jsonify({'error': 'Cannot parse request body as JSON'}), 400)

    # Make sure the program has less than 65536 characters
    if not validate(programs):
        return make_response(jsonify({'error': 'Program too big'}), 400)

    # Try to insert status into MongoDB
    try:
        doc_id = mongo_collection.insert_one({'status': 'SCHEDULED'}).inserted_id
    except Exception:
        logger.exception('Unable to insert status into MongoDB')
        return make_response('', 500)

    # Create a kubernetes job with files mounted as configmap, and deploy job
    job_definition = fill_template(str(doc_id), programs)

    try:
        kube_apply(job_definition, COMPILE_JOB_NAMESPACE)
    except Exception:
        logger.exception('Unable to dispatch compile job into Kubernetes for %s', doc_id)
        return make_response('', 500)

    # return id so client can poll the status of execution
    return jsonify({'_id': str(doc_id)})


@server.route('/status/<program_id>')
def status(program_id: str) -> Response:
    # Test if it is a valid id
    try:
        object_id = ObjectId(program_id)
    except InvalidId:
        return make_response(jsonify({'error': 'Invalid id'}), 400)

    # Search mongo for status
    doc = mongo_collection.find_one({'_id': object_id})

    if doc is None:
        return make_response(jsonify({'error': 'Program with this id was not found'}), 404)

    doc['_id'] = str(doc['_id'])

    return jsonify(doc)

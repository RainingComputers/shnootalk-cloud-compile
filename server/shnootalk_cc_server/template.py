from typing import Dict, List, Any

import yaml

from shnootalk_cc_server.config import MONGO_URL_SECRET_NAME, MONGO_URL_SECRET_KEY
from shnootalk_cc_server.config import MONGO_DATABASE, MONGO_COLLECTION
from shnootalk_cc_server.config import JOB_TIMEOUT

CONFIG_MAP = 0
JOB = 1


def fill_template(program_id: str, programs: Dict[str, str],
                  heartbeat: bool = False) -> List[Dict[str, Any]]:
    # Loads template file with kubernetes resource definition for a configmap and a job
    # Fills the configmap with program files to execute

    config_map_name = f'config-map-{program_id}'
    job_name = f'compile-job-{program_id}'

    with open('./shnootalk_cc_server/templates/job.yml', encoding='utf8') as yaml_f:
        job_template = list(yaml.safe_load_all(yaml_f))

    job_template[CONFIG_MAP]['metadata']['name'] = config_map_name
    job_template[CONFIG_MAP]['data'] = programs

    job_template[JOB]['metadata']['name'] = job_name

    job_template_spec = job_template[JOB]['spec']['template']['spec']

    job_template_env = job_template_spec['containers'][0]['env']

    job_template_env[0]['valueFrom']['secretKeyRef'] = {
        'name': MONGO_URL_SECRET_NAME,
        'key': MONGO_URL_SECRET_KEY
    }
    job_template_env[1]['value'] = MONGO_DATABASE
    job_template_env[2]['value'] = MONGO_COLLECTION
    job_template_env[3]['value'] = JOB_TIMEOUT
    job_template_env[4]['value'] = 'true' if heartbeat else 'false'

    job_template_spec['containers'][0]['command'][-1] = program_id

    job_template_spec['volumes'][0]['configMap']['name'] = config_map_name

    return job_template

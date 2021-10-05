from typing import Dict, List, Any

from copy import deepcopy

from shnootalk_cc_server.api_v1 import fill_template


def test_fill_template(test_job_template: List[Dict[str, str]],
                       test_programs: Dict[str, str]) -> None:
    assert fill_template('613c7fcf1cbaaff506b1084c', test_programs) == test_job_template


def test_fill_template_heartbeat(test_job_template: List[Dict[str, Any]],
                                 test_programs: Dict[str, str]) -> None:
    heartbeat_job_template = deepcopy(test_job_template)
    heartbeat_job_template_spec = heartbeat_job_template[1]['spec']['template']['spec']
    heartbeat_job_template_spec['containers'][0]['env'][4]['value'] = 'true'

    assert fill_template('613c7fcf1cbaaff506b1084c', test_programs, True) == heartbeat_job_template

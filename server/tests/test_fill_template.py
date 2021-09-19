from typing import Dict, List

from shnootalk_cc_server.api_v1 import fill_template


def test_fill_template(test_job_template: List[Dict[str, str]],
                       test_programs: Dict[str, str]) -> None:
    assert fill_template('613c7fcf1cbaaff506b1084c', test_programs) == test_job_template

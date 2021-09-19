from typing import Dict, List, Any

import kubernetes
from kubernetes.utils.create_from_yaml import create_from_dict


def kube_apply(kube_defs: List[Dict[str, Any]]) -> None:
    # Accepts a list of kubernetes resources definition and applies to cluster
    for definition in kube_defs:
        with kubernetes.client.ApiClient() as api_client:
            create_from_dict(api_client, definition)

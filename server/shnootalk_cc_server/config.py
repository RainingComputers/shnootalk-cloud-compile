import os
from kubernetes.config import load_kube_config, load_incluster_config
from pymongo import MongoClient

USE_INCLUSTER_CONFIG = os.getenv('USE_INCLUSTER_CONFIG', default='false')
KUBE_CONTEXT = os.getenv('KUBE_CONTEXT', default='k3d-shnootalk-cloud-compile')
MONGO_URL = os.getenv('MONGO_URL', default='mongodb://root:example@localhost:27017')
MONGO_DATABASE = os.getenv('MONGO_DATABASE', default='shnootalk-cloud-compile')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'job-output')

mongo_collection = MongoClient(MONGO_URL)[MONGO_DATABASE][MONGO_COLLECTION]

if USE_INCLUSTER_CONFIG == 'true':
    load_incluster_config()
else:
    load_kube_config(context=KUBE_CONTEXT)

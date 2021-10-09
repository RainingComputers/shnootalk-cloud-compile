class Messages:
    PROG_TOO_BIG_OR_INVALID_NAME_OR_JSON = \
        'Program too big or file names are wrong or invalid JSON'

    CANNOT_PARSE = 'Cannot parse request body as JSON'

    UNABLE_TO_INSERT = 'Unable to insert status into MongoDB'

    UNABLE_TO_SPAWN_JOB = 'Unable to dispatch compile job into Kubernetes for %s'

    UNABLE_TO_SPAWN_HEARTBEAT = 'Unable to dispatch hearbeat job into Kubernetes for %s'

    INVALID_ID = 'Invalid id'

    PROG_NOT_FOUND = 'Program with this id was not found'

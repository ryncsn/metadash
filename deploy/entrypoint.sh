#!/bin/bash
WORKER_MODE=false

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

_error() {
    echo -e ${RED}$1${NC} > /dev/stderr; exit 1;
}

_info() {
    echo -e ${GREEN}$1${NC} > /dev/stdout
}

function _pipenv () {
    ($(command -v pipenv) --version &>/dev/null && (pipenv $@; return $?))
}

while [ $# -gt 0 ]
do
    case $1 in
        --debug )
            DEBUG=true
            ;;
        --worker )
            WORKER_MODE=true
            ;;
        --beat-worker )
            BEAT_MODE=true
            ;;
        -h | --help )
            echo "usage: $0 [-h]
            options:
            --debug         Enable debug options
            --worker        Start celery worker
            --beat-worker   Start celery beat worker
            "
            exit 0
            ;;
    esac
    shift
done

if [[ $BEAT_MODE == 'true' ]] ; then
    _pipenv run celery worker -A metadash.async.task.celery -l info -B
elif [[ $WORKER_MODE == 'true' ]] ; then
    _pipenv run celery worker -A metadash.async.task.celery -l info
else
    _info "***Initilize Database if not initialized***"
    _pipenv run bin/md-manager db migrate

    _info "***Migrate Database if an older version of Database is present***"
    # TODO: not doing anything yet

    _pipenv run gunicorn -c deploy/gunicorn.py wsgi
fi

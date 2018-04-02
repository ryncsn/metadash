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

function _python () {
    ($(command -v python3) --version &>/dev/null && (python3 $@; return $?)) ||
    ($(command -v python) --version &>/dev/null && (python $@; return $?))
}

while [ $# -gt 0 ]
do
    case $1 in
        --venv )
            VENV=true && shift
            VENV_PATH=$1
            if [[ -z $VENV_PATH ]] ; then
                echo "VENV_PATH" is required
            fi
            ;;
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
            echo "usage: setup.sh [-h] [--venv VENV_PATH]
            options:
            --venv      Enter a virtualenv before run server
            --debug     Enable debug options
            "
            exit 0
            ;;
    esac
    shift
done

if [[ $VENV == 'true' ]] ; then
    $(command -v virtualenv &> /dev/null) || _error "'virtualenv' is needed but not installed"
    source $VENV_PATH/bin/activate
fi

if [[ $BEAT_MODE == 'true' ]] ; then
    celery worker -A metadash.async.task.celery -l info -B
elif [[ $WORKER_MODE == 'true' ]] ; then
    celery worker -A metadash.async.task.celery -l info
else
    _info "***Initilize Database if not initialized***"
    _python manager.py initdb

    _info "***Migrate Database if an older version of Database is present***"
    # TODO: not doing anything yet

    uwsgi --ini docker/uwsgi.ini
fi

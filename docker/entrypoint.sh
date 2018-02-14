#!/bin/bash
WORKER_MODE=false

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

if [[ $WORKER_MODE == 'true' ]] ; then
    celery worker -A metadash.async.task.celery -l info -B
else
    uwsgi --ini docker/uwsgi.ini
fi

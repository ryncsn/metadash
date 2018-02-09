#!/bin/bash

case $1 in
    --venv )
        shift
        VENV=true
        VENV_PATH=$1 && shift
        if [[ -z $VENV_PATH ]] ; then
            echo "VENV_PATH" is required
        fi
        ;;
    --debug )
        DEBUG=true
        # TODO
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

if [[ $VENV == 'true' ]] ; then
    $(command -v virtualenv &> /dev/null) || _error "'virtualenv' is needed but not installed"
    virtualenv $VENV_PATH
    source $VENV_PATH/bin/activate
fi

uwsgi --ini docker/uwsgi.ini

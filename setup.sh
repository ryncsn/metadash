#!/bin/bash

NO_VENT=false
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

_error() {
    echo -e ${RED}$1${NC}; exit 1;
}

_info() {
    echo -e ${GREEN}$1${NC}
}

function _is_virtualenv_installed () {
    virtualenv --help &>/dev/null || _error "'virtualenv' is needed but not installed properly"
}

function _is_pip_installed () {
    pip &>/dev/null || _error "'pip' required but not installed properly, exiting"
}

function _is_npm_installed () {
    $(command -v npm &> /dev/null) || _error "'npm' is needed but not installed properly"
}

case $1 in
    --venv )
        shift
        VENV=true
        VENV_PATH=$1 && shift
        if [[ -z $VENV_PATH ]] ; then
            echo "VENV_PATH" is required
        fi
        ;;
    --dev )
        shift
        DEV=true
        ;;
    -h | --help )
        echo "usage: setup.sh [-h] [--venv VENV_PATH]
        options:
        --venv      Create a virtual env in given patch and install all python packages inside the virtual env.
        --dev       Install dev packages, or only production packages are installed.
        "
        exit 0
        ;;
esac

_is_pip_installed
_is_npm_installed

if [[ $VENV == 'true' ]] ; then
    _is_virtualenv_installed
    virtualenv $VENV_PATH
    source $VENV_PATH/bin/activate
fi

_info "***Installing requirements of Metadash***"
if [[ -f 'requirements.txt' ]]; then
    pip install -r requirements.txt
fi

if [[ $DEV == 'true' && -f 'requirements.dev.txt' ]]; then
    _info "Installing dev requirements of Metadash"
    pip install -r requirements.txt
fi

_info "***Installing requirements of Plugins***"
for file in ./metadash/plugins/*/requirements.txt; do
    if [[ -f $file ]]; then
        pip install -r $file
    fi
done

_info "***Install node packages***"
npm install

_info "***Rebuilding Assets***"
npm run build

_info "***Initialize Database***"
python manager.py initdb

_info "***Migrating Database***"
echo "//TODO Not implemented"

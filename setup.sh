#!/bin/bash -e

NO_VENT=false
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

function _pip () {
    _python -m pip $@
}

function _virtualenv () {
    _python -m virtualenv $@
}

function _ensure_virtualenv_installed () {
    _virtualenv --help &>/dev/null || _error "'virtualenv' is needed but not installed properly"
}

function _ensure_pip_installed () {
    _pip -V &>/dev/null || _error "'pip' required but not installed properly, exiting"
}

function _ensure_npm_installed () {
    $(command -v npm &> /dev/null) || _error "'npm' is needed but not installed properly"
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
        --dev )
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
    shift
done

_info "***Make sure required tools are installed***"
_ensure_pip_installed
_ensure_npm_installed

_info "***Create virtualenv if needed***"
if [[ $VENV == 'true' ]] ; then
    _ensure_virtualenv_installed
    _virtualenv $VENV_PATH
    source $VENV_PATH/bin/activate
fi

_info "***Installing requirements of Metadash***"
if [[ -f 'requirements.txt' ]]; then
    _pip install -r requirements.txt
fi

if [[ $DEV == 'true' && -f 'requirements.dev.txt' ]]; then
    _info "Installing dev requirements of Metadash"
    _pip install -r requirements.txt
fi

_info "***Installing requirements of Plugins***"
for file in ./metadash/plugins/*/requirements.txt; do
    if [[ -f $file ]]; then
        _pip install -r $file
    fi
done

_info "***Install node packages***"
npm install --production

_info "***Rebuilding Assets***"
npm run build

_info "***Initialize Database***"
python manager.py initdb

_info "***Building Docs***"
cd docs && make html && cd ..
cp -r ./docs/_build/html/* ./metadash/dist/docs/

_info "***Migrating Database***"
echo "//TODO Not implemented"

#!/bin/bash

NO_VENT=false


_error() {
    echo $1; exit 1;
}


function _python () {
    $(which python) $@
}


function _is_pip_installed () {
    _python -m pip 1>2 &>/dev/null || _error "'pip' required but not installed properly, exiting"
}

function _is_npm_installed () {
    $(command -v npm &> /dev/null) || _error "'npm' is needed but not installed properly"
}

function _pip() {
    _python -m pip $@
}

function _npm() {
    npm $@
}

case $1 in
    --no-venv )
        NO_VENT=true
        shift
        ;;
esac

_is_npm_installed
_is_pip_installed

echo "Installing requirements of Metadash"
if [[ -f 'requirements.txt' ]]; then
    _pip install -r requirements.txt
fi

echo "Installing requirements of Plugins"
for file in ./metadash/plugins/*/requirements.txt; do
    if [[ -f $file ]]; then
        _pip install -r $file
    fi
done

echo "Rebuilding Assets"
_npm run build

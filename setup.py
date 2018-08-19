#!/usr/bin/env python
# -*- coding: utf-8 -*-


import glob
import sys
import subprocess

RED = '\033[0;31m'
GREEN = '\033[0;32m'
NC = '\033[0m'

DEV = False
ONLY_DEP = False


for arg in sys.argv:
    if arg == '--dev':
        DEV = True
    if arg == '--only-dependency':
        ONLY_DEP = True


def error(msg):
    print("{}{}{}".format(RED, msg, NC))


def info(msg):
    print("{}{}{}".format(GREEN, msg, NC))


try:
    info("*** Installing requirements of Metadash ... ***")
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
    if DEV:
        subprocess.run(['pip', 'install', '-r', 'requirements.dev.txt'])
    info("*** Installing requirements of Metadash Done ***")

    info("*** Installing requirements of Metadash Plugins ... ***")
    for filename in glob.iglob('metadash/plugins/*/requirements.txt'):
        subprocess.run(['pip', 'install', '-r', filename])
    if DEV:
        for filename in glob.iglob('metadash/plugins/*/requirements.dev.txt'):
            subprocess.run(['pip', 'install', '-r', filename])
    info("*** Installing requirements of Metadash Plugins Done ***")

    info("*** Install node packages ***")
    if DEV:
        subprocess.run(['npm', 'install'])
    else:
        subprocess.run(['npm', 'install', '--production'])
    info("*** Install node packages Done ***")

    if ONLY_DEP:
        info("*** Only install dependencies, exiting ***")
        sys.exit(0)

    info("*** Building Asserts ***")
    subprocess.run(['npm', 'run', 'build'])
    info("*** Building Asserts Done ***")

except Exception as err:
    error("Failed with exception:")
    raise

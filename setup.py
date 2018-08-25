#!/usr/bin/env python
# Pack it as a package for some rare case usage
# Be sure to install only in a virtualenv
# It is not supposed to be install as a common package at all

import glob
from setuptools import setup, find_packages
from manager import do_initialize


def read_file(file_name):
    with open(file_name) as file:
        return file.read()


def find_all_requirements(develop=False):
    requirements = {read_file('requirements.txt').splitlines()}
    if develop:
        requirements.update(read_file('requirements.dev.txt').splitlines())
    for filename in glob.glob('metadash/plugins/*/requirements.txt'):
        requirements.update(read_file(filename).splitlines())
        if develop:
            for filename in glob.glob('metadash/plugins/*/requirements.dev.txt'):
                requirements.update(read_file(filename).splitlines())
    return requirements


setup_params = dict(
    name='metadash',
    version='1.0',
    author='Kairui Song',
    author_email='ryncsn@gmail.com',
    license='GPLv3',
    python_requires='>=3.5',
    install_requires=find_all_requirements(),
    packages=find_packages(),
    package_data={
        '': [
            'config/*',
            'dist/*',
            'dist/*/*',
            'dist/*/*/*',
            'plugins/*/*.json',
        ],
    },
    scripts=[
        'bin/md-manager',
    ],
)


if __name__ == '__main__':
    do_initialize(dev=False, inst_py_dep=False, inst_node_dep=True, build_assert=True)
    setup(**setup_params)

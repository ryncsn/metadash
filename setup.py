#!/usr/bin/env python
# Pack it as a package for some rare case usage
# Be sure to install only in a virtualenv
# It is not supposed to be install as a common package at all

import glob
import sys
import subprocess

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install


def read_file(file_name):
    with open(file_name) as file:
        return file.read()


def find_all_requirements(develop=False):
    requirements = set(read_file('requirements.txt').splitlines())
    if develop:
        requirements.update(read_file('requirements.dev.txt').splitlines())
    for filename in glob.glob('metadash/plugins/*/requirements.txt'):
        requirements.update(read_file(filename).splitlines())
        if develop:
            for filename in glob.glob('metadash/plugins/*/requirements.dev.txt'):
                requirements.update(read_file(filename).splitlines())
    return list(requirements)


class DevelopCommand(develop):
    def run(self):
        subprocess.run(['bin/md-manager', 'setup', '--only-build', '--develop'])
        develop.run(self)


class InstallCommand(install):
    def run(self):
        subprocess.run(['bin/md-manager', 'setup', '--only-build'])
        install.run(self)


setup_params = dict(
    name='metadash',
    version='1.0',
    author='Kairui Song',
    author_email='ryncsn@gmail.com',
    license='GPLv3',
    python_requires='>=3.5',
    install_requires=find_all_requirements(),
    packages=find_packages(),
    cmdclass={
        'develop': DevelopCommand,
        'install': InstallCommand,
    },
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
    setup(**setup_params)

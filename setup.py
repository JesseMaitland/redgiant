import os
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install


VERSION = '0.0.1'


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(tag, VERSION)
            sys.exit(info)


def readme():
    with open('README.md') as file:
        return file.read()


setup(
    name='redgiant',
    version=VERSION,
    author='Jesse Maitland',
    discription='A collection of tools to help you manage your redshift projects',
    include_package_data=True,
    packages=find_packages(exclude=('tests*', 'venv')),
    entry_points={'console_scripts': ['red-dwarf = red_dwarf.__main__:main',
                                      'gatekeeper = redgiant.gatekeeper.__main__:main']},
    python_requires='>=3'
)

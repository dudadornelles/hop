from setuptools import setup, find_packages
import os

setup(
    name='hop-cli',
    version='0.0.0',
    description='Bootstrap your gocd setup using pipeline-as-code with hop.',
    url='https://github.org/dudadornelles/hop',
    author='Duda Dornelles',
    author_email='duda@hop-ci.com',
    packages=find_packages(exclude=['contrib', 'docs', 'test*']),
    install_requires=['boto3',
                      'ruamel.yaml', 
                      'docker',
                      'requests',
                      'gomatic',
                      'sh'],
    entry_points={
        'console_scripts': [
            'hop=hop:run',
        ],
    },
)


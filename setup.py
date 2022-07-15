#!/usr/bin/env python

"""The setup script."""
import os
import re
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open(os.path.join('qfieldlayout', '__init__.py')) as ver_file:
    for line in ver_file:
        if line.startswith('__version__'):
            version = re.sub("'", "", line[line.index("'"):]).rstrip()

requirements = ['numpy']

test_requirements = [ ]

setup(
    author="Dexter Pratt",
    author_email='depratt@ucsd.edu',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    description="Q Field layout algorithm",
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='qfieldlayout',
    name='qfieldlayout',
    packages=find_packages(include=['qfieldlayout', 'qfieldlayout.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/idekerlab/qfieldlayout',
    version=version,
    zip_safe=False,
)

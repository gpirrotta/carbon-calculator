#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
import os
import re
import sys

PY3 = sys.version_info[0] == 3
HERE = os.path.dirname(os.path.abspath(__file__))


def get_version():
    filename = os.path.join(HERE, 'carbon', '__init__.py')
    with open(filename) as f:
        contents = f.read()
    pattern = r"^__version__ = \"(.*?)\"$"
    return re.search(pattern, contents, re.MULTILINE).group(1)
    


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()


test_requirements = [ ]

setup(
    author="Giovanni Pirrotta",
    author_email='giovanni.pirrotta@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Carbon Calculator",
    install_requires=required,
    license="MIT license",
    long_description=readme,
    long_description_content_type='text/markdown',
    py_modules = ["carboncli"],
    platforms='any',
    include_package_data=True, 
    keywords='green,environment,carbon,co2,pollution',
    name='carbon-calculator',
    packages=find_packages(include=['carbon', 'carbon.*']),
    tests_require=test_requirements,
    url='https://github.com/gpirrotta/carbon-calculator',
    version=get_version(),
    zip_safe=False,
    entry_points = {
        'console_scripts': ['carbon-cli=carboncli:main'],
    }
)

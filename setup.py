import os
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'Opensim',
    version = '1.0.1',
    author = 'Copenhagen Atomics',
    author_email = 'lorenzo.chierici@copenhagenatomics.com',
    description = 'OpenMC customized toolkit simulation',
    url = 'https://github.com/church89/opensim',
    long_description = long_description,
    packages = find_packages(),
    include_package_data = True,
    package_data = {
        'sim.data.materials.msre': ['*.csv'],
        'sim.data.materials.are': ['*.csv'],
        'sim.data.materials.zpre': ['*.csv']
    },

    entry_points={
        'console_scripts': ['simrun=sim.__main__:main']
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering'
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
    install_requires=[
        #'openmc' needed, but not available on pip
        #'pymoab' needed, but not available on pip
        'pandas',
        'numpy',
        'matplotlib'
    ]
)

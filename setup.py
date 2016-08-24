# -*- coding: utf-8 -*-

import os
from setuptools import setup, Command

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system('rm -vrf ./build ./*.egg-info')
        os.system('find . -type f -name "*.pyc" -exec rm -vf {} \;')


setup(
    name='dtk',
    version='1.0',
    description='Dispersion toolkits',
    author='Ming-Hong Bai',
    author_email='mhbai.tw@gmail.com',
    url='https://github.com/mhbai/dtk.git',
	test_suite='dtk.tests',
    packages=['dtk'],
    cmdclass={
        'clean': CleanCommand,
    }
)



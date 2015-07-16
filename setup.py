#!/usr/bin/env python
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        pytest.main(self.test_args)

requirements = [
    'addict',
]


setup(
    name='morf',
    version='0.0.1',
    url='https://www.github.com/cieplak/morf',
    author='patrick cieplak',
    author_email='patrick.cieplak@gmail.com',
    description='schema transformation library',
    packages=['morf'],
    license=open('LICENSE').read(),
    include_package_data=True,
    install_requires=requirements,
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
)

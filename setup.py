#!/usr/bin/env python

from setuptools import setup, find_packages
import os
import multiprocessing, logging  # AJ: for some reason this is needed to not have "python setup.py test" freak out

module_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    setup(
        name='chronograph',
        version='0.0.1',
        description='Chronograph is a simple stopwatch / chronometer / chronograph for timing Python code.',
        long_description=open(os.path.join(module_dir, 'README.rst')).read(),
        url='https://github.com/computron/chronograph',
        author='Anubhav Jain',
        author_email='anubhavster@gmail.com',
        license='MIT',
        packages=find_packages(),
        package_data={},
        zip_safe=False,
        install_requires=[],
        extras_require={},
        classifiers=['Programming Language :: Python :: 2.7',
                     'Development Status :: 4 - Beta',
                     'Intended Audience :: Developers',
                     'Operating System :: OS Independent',
                     'Topic :: Utilities'],
        test_suite='nose.collector',
        tests_require=['nose'],
        scripts=[]
    )

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'turbo>=0.4.5',
    'mistune',
]

test_requirements = [
]

setup(
    name='turbo_markdown',
    version='0.3.0',
    description="A cli tool to view local markdown files",
    long_description=readme + '\n\n' + history,
    author="wecatch",
    author_email='zhyq0826@126.com',
    url='https://github.com/wecatch/turbo_markdown',
    packages=[
        'turbo_markdown',
    ],
    package_dir={'turbo_markdown':
                 'turbo_markdown'},
    entry_points={
        'console_scripts': [
            'turbo-markdown=turbo_markdown.cli:main'
        ]
    },
    include_package_data=True,
    package_data={'turbo_markdown': [
        'static/js/*', 'static/css/*', 'static/img/*']},
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='markdown,turbo',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)

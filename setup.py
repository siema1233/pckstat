from setuptools import setup

setup(
    name="Package Statistics",
    version='0.0.1',
    packages=['pckstat'],
    install_requires=[
        'Click',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        pckstat=pckstat.cli:pckstat
    ''',
)
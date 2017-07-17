from setuptools import setup

setup(
    name='psn',
    version='0.0.1',
    packages=['psn'],
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'psn-notifier = psn.cli:main',
        ],
    },
)

from setuptools import setup

from viewer.__version__ import VERSION


with open('requirements.txt') as f:
    REQUIRED = f.read().splitlines()


setup(
    name='live-viewer',
    version=VERSION,
    py_modules=['viewer'],
    install_requires=REQUIRED,
    entry_points='''
        [console_scripts]
        live-viewer=viewer.cli:cli
    ''',
)

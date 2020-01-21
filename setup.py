from setuptools import setup


with open('requirements.txt') as f:
    REQUIRED = f.read().splitlines()


setup(
    name='live-viewer',
    version='0.1.0',
    py_modules=['server'],
    install_requires=REQUIRED,
    entry_points='''
        [console_scripts]
        live-viewer=server.cli:cli
    ''',
)

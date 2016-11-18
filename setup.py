from distutils.core import setup

setup(
    name='cthulhuwars',
    version='0.1dev',
    author='MountainsOfMadness',
    author_email='masterblasterofdisaster@gmail.com',
    packages=['cthulhuwars'],
    entry_points={
        'CWServer': 'cthulhuwars.CWServer = cthulhuwars.server:CWServer',
        'CWClient': 'cthulhuwars.CWClient = cthulhuwars.server:CWClient',,
    },
    license='LICENSE',
    description="An implementation of Cthulhu Wars.",
)

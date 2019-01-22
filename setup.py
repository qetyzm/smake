from setuptools import setup

setup(
    name="smake_buildtools",
    version="0.1.1",
    packages=['smake_buildtools'],
    entry_points={
    },
    install_requires=[
        'platform',
        'glob',
        'subprocess'
    ],
    description='Simple Make replacement for developers who love Python',
    author='Qetyzm',
    author_email='qetyzm@gmail.com',
    url='https://github.com/qetyzm/smake',
    keywords=['packages', 'import', 'downloader', 'package-management'],
    license=open('LICENSE').read(),
    long_description=open('README.md').read()
)

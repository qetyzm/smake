from setuptools import setup

setup(
    name="smake",
    version="0.1.0",
    packages=['smake-buildtools'],
    entry_points={
        'console_scripts': [
            'smake = smake.__main__:main'
        ]
    },
    install_requires=[
     
    ],
    description='Simple dependency downloader and Make replacement',
    author='Qetyzm',
    author_email='qetyzm@gmail.com',
    url='https://github.com/qetyzm/smake',
    keywords=['packages', 'import', ''],
    license=open('LICENSE').read(),
    long_description=open('README.md').read()
)

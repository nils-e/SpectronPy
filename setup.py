import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='SpectronPy',
    version='1.0',
    author="Nils Rognerud",
    author_email="TBD",
    description=("An demonstration of how to create, document, and publish "
                 "to the cheese shop a5 pypi.org."),
    license="BSD",
    keywords="spectron electron python selenium webdriver",
    url="TBD",
    packages=find_packages(),
    long_description=read('readme.md'),
    python_requires='>=3.10',
    install_requires=[
        'selenium==4.3.0',
        'dataclasses==0.6',
        'psutil==5.9.1',
        'webdriver_manager==3.8.3',
        'behave~=1.2.6',
        'behave-html-formatter==0.9.10',
    ]
)

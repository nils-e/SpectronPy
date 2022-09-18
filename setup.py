import os

from setuptools import setup, find_packages, Command


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info ./*.png ./*.log')


setup(
    name='SpectronPy',
    version='0.1.3',
    author="Nils",
    license="MIT",
    keywords="spectronpy spectron electron python selenium webdriver",
    url="https://github.com/nils-e/SpectronPy",
    packages=['spectronpy'],
    package_dir={'spectronpy': 'lib'},
    long_description=read('readme.md'),
    long_description_content_type='text/markdown',
    include_package_data=True,
    python_requires='>=3.10',
    install_requires=[
        'selenium==4.4.3',
        'dataclasses==0.6',
        'psutil==5.9.1',
        'webdriver_manager==3.8.3',
    ],
    cmdclass={
        'clean': CleanCommand,
    },
)

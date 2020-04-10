# File : setup.py
# Created by gabys
# Date : 10/04/2020
# License : Apache 2.0

import setuptools

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('VERSION') as f:
    version = f.read().strip()

setuptools.setup(
    name='gsynch',
    version=version,
    description='gSynch allows you to synchronise your Git repository with your Steam Workshop publication in few '
                'clicks.',
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Gabriel Santamaria",
    author_email="gaby.santamaria@outlook.fr",
    url="https://github.com/Gabyfle/gSynch",
    license=license,
    packages=setuptools.find_packages(exclude=("tests", "docs"))
)

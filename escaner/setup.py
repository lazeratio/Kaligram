from distutils.core import setup
from setuptools import find_packages

setup(
    name='Kaligram',
    version='0.1.0',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    url='https://github.com/lazeratio',
    license='GPL v3',
    author='lazeratio',
    author_email='',
    entry_points={
        'console_scripts': ['xknr=xknr:main'],
    },
    description='Escaner de red con extracción de información mediante módulos personalizables'
)

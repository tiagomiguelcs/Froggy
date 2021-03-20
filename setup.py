from setuptools import setup
import os

with open('requirements.txt') as f: 
    required = f.read().splitlines()

setup(
    name='froggy',
    version='0.0.1',    
    description='A keep it simple, stupid (KISS) framework for the development of REST-based services.',
    url='https://github.com/tiagomiguelcs/froggy',
    author='Tiago Simões',
    author_email='tiago.simoes@ubi.pt',
    license='Apacha License 2.0',
    packages=['froggy'],
    install_requires=required,
    classifiers=[
        'Intended Audience :: Science/Research',
        'Operating System :: Windows :: Linux :: MacOS',        
        'Programming Language :: Python :: 3',
    ],
)

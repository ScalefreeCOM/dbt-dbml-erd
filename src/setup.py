from setuptools import setup, find_packages

setup(
    name='dbterd',
    version='0.0.1',    
    description='A simple package that can generate dbml file and erd diagrams for dbt',
    url='initial version at https://github.com/intellishore/dbt-erdiagram-generator',
    author='Marvin Geerken (initial version by Oliver Rise Thomsen and Anders Boje Hertz)',
    author_email='marvin.geerken.ext@siemens.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['Click'],
    
    entry_points='''
        [console_scripts]
        dbterd=dbterd.terminal:cli
    ''',
)

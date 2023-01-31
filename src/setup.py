from setuptools import setup, find_packages

setup(
    name='erdbt',
    version='0.1.0',    
    description='An application to generate a dbml file out of your dbt artifacts and visualizes it as an Entity Relationship Diagram.',
    url='https://github.com/ScalefreeCOM/dbt_dbml_erd (initial version https://github.com/intellishore/dbt-erdiagram-generator)',
    author='Marvin Geerken (initial version by Oliver Rise Thomsen and Anders Boje Hertz)',
    author_email='mgeerken@scalefree.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['Click'],
    
    entry_points='''
        [console_scripts]
        erdbt=erdbt.terminal:cli
    ''',
)

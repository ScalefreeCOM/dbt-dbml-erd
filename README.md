# dbt_dbml_erd
Python application to create Entity Relationship Diagrams in dbt projects.

There are some great ways to auto generate ERD diagrams. Thus, we just want to build a bridge between dbt and these tools. This is done by converting the dbt manifest and catalog to a dbml files. From this dbml file a ERD diagram can be created with a tool like [dbdocs](https://dbdocs.io/). 

# Installation

1. Clone this repository to a folder and run:

```
pip install src/
```

or direct from git

```
pip install -U git+https://github.com/ScalefreeCOM/dbt_dbml_erd#subdirectory=src
```

2. Setup dbdocs cli for diagram creations. [Instructions here](https://dbdocs.io/docs)
3. Test dbterd with the following command:
```
dbterd tests/manifest.json tests/catalog.json test.dbml test True
```
# Usage
To use this packages on your own project run *dbterd* with the following parameters in order: 

1. Path to the dbt manifest 
2. Path to the dbt catalog 
3. Path to store the dbml file
4. Name of the project on dbdocs.io
5. True or False if you want to vizualise the dbml file on dbdocs.io
6. (optional) Name of your relationships test 


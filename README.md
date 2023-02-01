# dbt_dbml_erd
A Python application that creates Entity Relationship Diagrams (ERDs) in dbt projects using the open-source dbml language and the [dbdocs](https://dbdocs.io/) tool for visualization.

The app requires the following artifacts to create the dbml file:
- `manifest.json`
- `catalog.json`

It should be noted that the information about relationships comes from the dbt relationships test and therefore the tool only works if these tests are implemented.

## Installation

1. Clone this repository and navigate to the `src` folder. Run:

```
pip install
```

or install directly from git using the following command:

```
pip install -U git+https://github.com/ScalefreeCOM/dbt_dbml_erd#subdirectory=src
```

2. Set up the dbdocs cli for diagram creation by following the [instructions here](https://dbdocs.io/docs)
3. Test the tool by running the following command:

```
erdbt tests/manifest.json tests/catalog.json test.dbml test True
```

## Usage

To use this application in your own project, run the `erdbt` command with the following parameters in order:

1. Path to the dbt `manifest.json`
2. Path to the dbt `catalog.json`
3. Path and file name to store the dbml file
4. Name of the project on dbdocs.io
5. `True` or `False` if you want to visualize the dbml file on dbdocs.io
6. (optional) Name of your relationships test

Example:

```
erdbt my_project/manifest.json my_project/catalog.json my_project/erd.dbml my_project_erd True my_project_relationships
```

This command will generate an ERD file named `erd.dbml` in the `my_project` folder, using the `manifest.json` and `catalog.json` files also located in that folder. The ERD will be uploaded to dbdocs.io under the project name `my_project_erd` and using the relationships test named `my_project_relationships`.
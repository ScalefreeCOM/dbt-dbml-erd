import json
import logging


def loadModel(catalog_path, manifest_path):
    """Loads the dbt catalog and manifest files. The manifest selected is the one that will be used to generate the ERD diagram.

    Args:
        catalog_path (Path): Path to the dbt catalog file in JSON format
        manifest_path (Path): Path to the dbt manifest file in JSON format

    Returns:
        tuple: A tuple containing the loaded catalog and manifest dictionaries
    """
    try:
        with open(catalog_path) as f:
            catalog = json.load(f)
    except Exception as e:
        logging.error(f"Error loading the catalog from {catalog_path}: {e}")
        raise
    try:
        with open(manifest_path) as f:
            manifest = json.load(f)
    except Exception as e:
        logging.error(f"Error loading the manifest from {manifest_path}: {e}")
        raise

    return catalog, manifest


def createTable(dbml_path, model):
    """Create a table in the dbml file.

    Args:
        dbml_path (Path): The file path where the table will be stored in dbml format
        model (dict): The dbt model to extract the table and columns from

    """
    name = model["metadata"]["name"].lower()
    schema = model["metadata"]["schema"].lower()
    columns = list(model["columns"].keys())
    start = "{"
    end = "}"

    dbml_path.write(f"Table {schema}.{name} as {name} {start} \n")

    for column_name in columns:
        column = model["columns"][column_name]
        name = column["name"].lower()
        dtype = column["type"].lower()

        dbml_path.write(f"{name} {dtype} \n")
    dbml_path.write(f"{end} \n")


def relatedModels(manifest, test_name):
    """Returns a list of related models, that will be used to limit the table created out of the catalog.

    Args:
        manifest (dict): The dbt manifest holding the relationships
        test_name (str): Name of the relationship test

    Returns:
        list: A list of related models
    """
    related_models = []

    for node in manifest["nodes"].values():
        if "test_metadata" in node and node["test_metadata"].get("name").lower() == test_name.lower():
            related_models.append(node["refs"][0][0].lower())
            related_models.append(node["refs"][1][0].lower())

    related_models = list(set(related_models))

    return related_models


def createRelatonship(dbml_path, manifest, test_name):
    """Create a relationship in the dbml file. Loops over all columns to find relationship tests and saves them to the dbml file

    Args:
        dbml_path (Path): The file path where the relationships will be stored in dbML format
        manifest (dict): The dbt manifest to extract relationships from
        test_name (str): Name of the relationship test
    """
    rel_list = []

    for node in manifest["nodes"].values():
        if "test_metadata" in node and node["test_metadata"]["name"].lower() == test_name.lower():
            rel_list.append((node["refs"][0][0].lower(), node["test_metadata"]["kwargs"]["field"].lower(),
                             node["refs"][1][0].lower(), node["test_metadata"]["kwargs"]["column_name"].lower()))

    rel_list = list(set(rel_list))

    for rel in rel_list:
        dbml_path.write(f"Ref: {rel[0]}.{rel[1]} <> {rel[2]}.{rel[3]} \n")


def genereatedbml(manifest_path, catalog_path, dbml_path, test_name):
    """Create a dbml file for a dbt manifest.

    Args:
        manifest_path (Path): Path to the dbt manifest file
        catalog_path (Path): Path to the dbt catalog file
        dbml_path (Path): Path and file name of the generated dbml file (e.g. "/path/to/file.dbml")
        test_name (str): Name of the relationship test to be used to extract relationships from the dbt manifest.

    Returns:
        None: A dbml file is created and stored in the specified `dbml_path`
    """
    catalog, manifest = loadModel(catalog_path, manifest_path)
    model_names = sorted(list(catalog["nodes"].keys()))

    related_models = relatedModels(manifest, test_name)

    with open(dbml_path, "w") as dbml_file:
        for model_name in model_names:
            model = catalog["nodes"][model_name]
            if model["metadata"]["name"].lower() in related_models:
                createTable(dbml_file, model)
        createRelatonship(dbml_file, manifest, test_name)
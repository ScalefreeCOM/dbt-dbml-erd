import json
import re

def loadModel(catalog_path, manifest_path):
    """Loads the dbt catalog and manifest. The manifest selected is the one that will be used to generate the ERD diagram.

    Args:
        catalog_path (Path): Path to dbt catalog
        manifest_path (Path): Path to dbt manifest

    Returns:
        dict, dict: Return manifest and catalog dicts.  
    """    
    with open(catalog_path) as f:
        catalog = json.load(f)


    with open(manifest_path) as f:
        manifest = json.load(f)

    return catalog, manifest


def createTable(dbml_path, model):
    """Create a table in the dbml file. 

    Args:
        dbml_path (dbml file): The file where to store the table
        model (dbt model): The dbt model to extract the table and columns from
    """    
    name = model["metadata"]["name"]
    schema = model["metadata"]["schema"]
    columns = list(model["columns"].keys())
    start = "{"
    end = "}"

    dbml_path.write(f"Table {schema}.{name} as {name} {start} \n")

    for column_name in columns:
        column = model["columns"][column_name] 
        name = column["name"]
        dtype = column["type"]

        dbml_path.write(f"{name} {dtype} \n")
    dbml_path.write(f"{end} \n")


def relatedModels(manifest, test_name):
    """Returns a list of related models, that will be used to limit the table created out of the catalog.json.

    Args:
        manifest: Manifest holding the relationships

    Returns:
        list: Return related models list.  
    """    
    related_models = []

    for node in manifest["nodes"].values():
        if "test_metadata" in node:
            if node["test_metadata"]["name"] == test_name:
                related_models.append(node["refs"][0][0].upper())
                related_models.append(node["refs"][1][0].upper())

    return related_models
    
def createRelatonship(dbml_path, manifest, test_name):
    """Create a relationship in the dbml file. Loops over all columns to find relationship tests and saves them to the dbml file

    Args:
        dbml_path (dbml file): The file where to store the table
        manifest (dbt manifest): The dbt manifest to extract relationships from    
    """                 
    rel_list = []

    for node in manifest["nodes"].values():
        if "test_metadata" in node:
            if node["test_metadata"]["name"] == test_name:
                rel_list.append((node["refs"][0][0].upper(), node["refs"][1][0].upper(), node["test_metadata"]["kwargs"]["field"].upper()))
    
    rel_list = list(set(rel_list))

    for rel in rel_list:
        dbml_path.write(f"Ref: {rel[0]}.{rel[2]} <> {rel[1]}.{rel[2]} \n")

def genereatedbml(manifest_path, catalog_path, dbml_path, test_name):
    """Create dbml file for a dbt manifest

    Args:
        catalog_path (Path): Path to dbt catalog
        manifest_path (Path): Path to dbt manifest
        dbml_path (Path): Pat to save dbml file
        test_name: Name of the relationship test
    """
    catalog, manifest = loadModel(catalog_path, manifest_path)
    model_names = sorted(list(catalog["nodes"].keys()))

    related_models = relatedModels(manifest, test_name)
    
    with open(dbml_path, "w") as dbml_file:
        for model_name in model_names:
            model = catalog["nodes"][model_name]
            if model["metadata"]["name"] in related_models: 
                createTable(dbml_file, model)        
        createRelatonship(dbml_file, manifest, test_name)
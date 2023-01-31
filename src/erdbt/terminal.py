import click
from .core import genereatedbml
import subprocess


@click.command()
@click.argument('manifest_path', type=str)
@click.argument('catalog_path', type=str)
@click.argument('erd_path', type=str)
@click.argument('project_name', type=str)
@click.argument('visualize', type=bool)
@click.argument('test_name', type=str, required=False, default="relationships")

def cli(manifest_path, catalog_path, erd_path, project_name, visualize, test_name):
    """"Generate a DBML file from a dbt project and visualize it with dbdocs.io"""
    try:
        genereatedbml(manifest_path, catalog_path, erd_path, test_name)
    except:
        print("The dbml file does not match the required format")
        
    if visualize:
        try:
            subprocess.run(f"dbdocs build {erd_path} --project {project_name}", text=True, shell=True)
        except:
            print("dbdocs is not set up probably")
            

import click
import subprocess
from .core import genereatedbml,process_file
@click.command()
@click.argument('manifest_path', type=str)
@click.argument('catalog_path', type=str)
@click.argument('erd_path', type=str)
@click.argument('project_name', type=str)
@click.argument('visualize', type=bool)
@click.argument('test_name', type=str, required=False, default="relationships")
def cli(manifest_path, catalog_path, erd_path, project_name, visualize, test_name):
    """
    Generate a DBML file for a dbt project and optionally visualize it with dbdocs.io
    """
    try:
        genereatedbml(manifest_path, catalog_path, erd_path, test_name)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except Exception as e:
        print(f"Error generating DBML file: {e}")
        return
    try:
        process_file(erd_path)
    except Exception as e:
        print(f"Error: {e}")
    if visualize:
        password = '$c@lefree123'
        try:
            result = subprocess.run(f"dbdocs build {erd_path} --project {project_name} --password {password}", text=True, shell=True, check=True)
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except subprocess.CalledProcessError as e:
            print(f"Error running dbdocs: {e}")
        except Exception as e:
            print(f"Error visualizing with dbdocs: {e}")
            


        

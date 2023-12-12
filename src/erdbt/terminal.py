import re 
import click
import subprocess
from .core import genereatedbml
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
        try:
            result = subprocess.run(f"dbdocs build {erd_path} --project {project_name}", text=True, shell=True, check=True)
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except subprocess.CalledProcessError as e:
            print(f"Error running dbdocs: {e}")
        except Exception as e:
            print(f"Error visualizing with dbdocs: {e}")
            

def process_file(file_path):
    """
    Validates a DBML file and removes problematic lines by overwrriting the generated .dbml file.
    Parameters:
        file_path (str): The file path of the DBML file to be validated and cleaned.
    Returns:
        None
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    existing_tables = set()
    for line in reversed(lines):
        match = re.match(r'^Table \S+\.\S+ as (\S+)', line)
        if match:
            table_name = match.group(1)
            existing_tables.add(table_name.strip())

    for i, line in enumerate(lines):
        if 'Ref:' in line:
            referenced_table_match0 = re.search(r'Ref:\s*([^<>\s]+)', line)
            referenced_table_match1 = re.search(r'(?<=>).*', line)
            if referenced_table_match0 :
                referenced_table_0 = referenced_table_match0.group(1).strip().split('.')[0]
                if referenced_table_0 not in existing_tables:
                    lines[i] = f'// {line}'
            if referenced_table_match1:
                referenced_table_1 = referenced_table_match1.group(0).strip().split('.')[0]
                if referenced_table_1 not in existing_tables:
                    lines[i] = f'// {line}'

    with open(file_path, 'w') as file:
        file.writelines(lines)
        

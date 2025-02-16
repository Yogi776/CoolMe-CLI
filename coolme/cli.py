import click
import os
import logging

# Set the directory for templates relative to this script's location
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s: ')

def load_template(template_path):
    """Load template content from a file."""
    if not os.path.exists(template_path):
        logging.error(f"Template file not found: {template_path}")
        return None
    with open(template_path, "r") as template_file:
        return template_file.read()

def create_folder_if_not_exists(folder_path):
    """Ensure a folder exists, create it if doesn't."""
    try:
        os.makedirs(folder_path, exist_ok=True)
        logging.info(f"Created directory: {folder_path}")
    except Exception as e:
        logging.error(f"Error creating directory '{folder_path}': {e}")

@click.group()
def cli():
    """CoolMe CLI - A tool to automate workflow and policy YAML creation."""
    pass

@click.group()
def create():
    """Create resources."""
    pass

@click.group(name="create")
def create_group():
    """Create resources like workflows and policies."""
    pass

@create_group.command(name="postgres-icebase")
@click.argument('project_name')
@click.argument('name')
@click.argument('ingestion_items', nargs=-1)
@click.option('--type', default="default", help="Type of ingestion, e.g., 'default' or 'postgres-icebase'")
@click.option('--output-catalog', default="default_catalog", help="Output catalog name")
@click.option('--output-schema', default="default_schema", help="Output schema name")
@click.option('--output-tables', type=lambda kv: {k:v for k, v in (x.split('=') for x in kv.split(','))}, required=True,
              help="Mapping of ingestion items to output tables")
@click.option('--template-path', default=os.path.join(TEMPLATES_DIR, "postgres-icebase.yaml"),
              help="Path to the ingestion template file")
def create_workflow(name,project_name, ingestion_items, type, output_catalog, output_schema, output_tables, template_path):
    """Create ingestion files based on a customizable template."""
    logging.info(f"Creating workflows for project: {project_name} with type: {type}")
    base_path = os.path.join(os.getcwd(), project_name, f"{name}/build/data-processing")
    create_folder_if_not_exists(base_path)

    for item in ingestion_items:
        output_table = output_tables.get(item, None)
        if not output_table:
            logging.error(f"No output table specified for {item}, skipping file creation.")
            continue

        template_content = load_template(template_path)
        if not template_content:
            logging.error("Failed to load the template content.")
            continue

        file_content = template_content.format(
            profile=item,
            ingestion_title=item.replace("_", " ").title(),
            output_catalog=output_catalog,
            output_schema=output_schema,
            output_table=output_table
        )

        file_path = os.path.join(base_path, f"wf-{item}-flare.yaml")
        with open(file_path, 'w') as file:
            file.write(file_content)
            logging.info(f"Created file: {file_path}")


@create_group.command(name="azure-postgres")
@click.option('--project_name', default="default", help="Project name")
@click.option('--data-product', default="default", help="Name of the data product")
@click.option('--entity', help="Comma-separated list of entities or ingestion items to include")
@click.option('--output-catalog', default="azure_catalog", help="Output catalog name for Azure PostgreSQL")
@click.option('--output-schema', default="azure_schema", help="Output schema name for Azure PostgreSQL")
@click.option('--output-tables', type=lambda kv: {k: v for k, v in (x.split('=') for x in kv.split(','))}, required=True,
              help="Mapping of entities to output tables for Azure PostgreSQL")
@click.option('--template-path', default=os.path.join(TEMPLATES_DIR, "azure-postgres.yaml"),
              help="Path to the Azure PostgreSQL ingestion template file")
def azure_postgres(project_name, data_product, entity, output_catalog, output_schema, output_tables, template_path):
    """Create ingestion files specifically configured for Azure PostgreSQL."""
    logging.info(f"Creating Azure PostgreSQL workflows for project: {project_name}, Data Product: {data_product}")
    base_path = os.path.join(os.getcwd(), project_name, f"{data_product}/build/data-processing")
    create_folder_if_not_exists(base_path)

    entities = entity.split(',') if entity else []
    for item in entities:
        output_table = output_tables.get(item.strip(), None)
        if not output_table:
            logging.error(f"No output table specified for {item}, skipping file creation.")
            continue

        template_content = load_template(template_path)
        if not template_content:
            logging.error("Failed to load the template content.")
            continue

        file_content = template_content.format(
            profile=item.strip(),
            ingestion_title=item.replace("_", " ").title(),
            output_catalog=output_catalog,
            output_schema=output_schema,
            output_table=output_table
        )

        file_path = os.path.join(base_path, f"config-{item.strip()}-postgres.yaml")
        with open(file_path, 'w') as file:
            file.write(file_content)
            logging.info(f"Created Azure PostgreSQL workflow file for {item.strip()}: {file_path}")
cli.add_command(create_group)
if __name__ == "__main__":
    cli()

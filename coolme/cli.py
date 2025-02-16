import click
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s: ')

# Define the directory for templates
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")

class IngestionManager:
    """
    Manages the creation of ingestion configuration files for different database environments.
    """
    def __init__(self, project_name, data_product, template_dir):
        self.project_name = project_name
        self.data_product = data_product
        self.template_dir = template_dir
        self.base_path = os.path.join(os.getcwd(), project_name, f"{data_product}/build/data-processing")
        self.create_folder_if_not_exists(self.base_path)

    def create_folder_if_not_exists(self, folder_path):
        """Creates a folder if it does not exist."""
        try:
            os.makedirs(folder_path, exist_ok=True)
            logging.info(f"Created directory: {folder_path}")
        except Exception as e:
            logging.error(f"Error creating directory '{folder_path}': {e}")

    def load_template(self, template_name):
        """Loads a template file from the specified path."""
        template_path = os.path.join(self.template_dir, f"{template_name}")
        if not os.path.exists(template_path):
            logging.error(f"Template file not found: {template_path}")
            return None
        with open(template_path, "r") as template_file:
            return template_file.read()

    def create_config_files(self, entities, output_catalog, output_schema, output_tables, template_name):
        """Creates configuration files for each entity based on the template."""
        template_content = self.load_template(template_name)
        if not template_content:
            logging.error("Failed to load the template content.")
            return

        for item in entities:
            output_table = output_tables.get(item.strip(), None)
            if not output_table:
                logging.error(f"No output table specified for {item}, skipping file creation.")
                continue

            file_content = template_content.format(
                profile=item.strip(),
                ingestion_title=item.replace("_", " ").title(),
                output_catalog=output_catalog,
                output_schema=output_schema,
                output_table=output_table
            )

            file_path = os.path.join(self.base_path, f"config-{item.strip()}.yaml")
            with open(file_path, 'w') as file:
                file.write(file_content)
                logging.info(f"Created configuration file for {item.strip()}: {file_path}")

@click.group()
def cli():
    """CoolMe CLI - A tool to automate workflow and policy YAML creation."""
    pass

def setup_create_command(env_name, default_catalog, default_schema, template_filename):
    @cli.command(name=f"create-{env_name}")
    @click.option('--project_name', default="default", help="Project name")
    @click.option('--data-product', default="default", help="Name of the data product")
    @click.option('--entity', help="Comma-separated list of entities or ingestion items to include")
    @click.option('--output-catalog', default=default_catalog, help=f"Output catalog name for {env_name}")
    @click.option('--output-schema', default=default_schema, help=f"Output schema name for {env_name}")
    @click.option('--output-tables', type=lambda kv: {k: v for k, v in (x.split('=') for x in kv.split(','))}, required=True,
                  help="Mapping of entities to output tables")
    @click.option('--template-path', default=os.path.join(TEMPLATES_DIR, template_filename),
                  help=f"Path to the {env_name} ingestion template file")
    def create_env_ingestion(project_name, data_product, entity, output_catalog, output_schema, output_tables, template_path):
        """
        CLI command to create ingestion files for specified entities using templates for {env_name}.
        """
        entities = entity.split(',') if entity else []
        manager = IngestionManager(project_name, data_product, os.path.dirname(__file__))
        manager.create_config_files(entities, output_catalog, output_schema, output_tables, template_path)

    return create_env_ingestion

# Setup commands for different environments
setup_create_command('azure-postgres', 'postgres', 'public', 'azure-postgres.yaml')
setup_create_command('postgres-icebase', 'icebase', 'default', 'postgres-icebase.yaml')

if __name__ == "__main__":
    cli()

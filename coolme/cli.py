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

class ConfigGenerator:
    """
    Manages the creation of configuration files based on templates.
    """
    def __init__(self, template_dir):
        self.template_dir = template_dir

    def load_template(self, template_name):
        """Load a YAML template from the specified path."""
        template_path = os.path.join(self.template_dir, f"{template_name}")
        try:
            with open(template_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            logging.error(f"Template file not found: {template_path}")
            return None

    def create_config(self, template_content, **kwargs):
        """Create a configuration file from a template and replace placeholders."""
        return template_content.format(**kwargs)

@click.group()
def cli():
    """CoolMe CLI - A tool to automate workflow and policy YAML creation."""
    pass

def setup_create_command(env_name, default_catalog, default_schema, template_filename):
    @cli.command(name=f"create-{env_name}")
    @click.option('--project_name', default="default", help="Project name")
    @click.option('--data-product', default="default", help="Name of the data product")
    @click.option('--entity', help="Comma-separated list of entities or ingestion items to include")
    @click.option('--output-catalog', default=default_catalog, help=f"Output catalog name for {default_catalog}")
    @click.option('--output-schema', default=default_schema, help=f"Output schema name for {default_schema}")
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

@click.command(name="create-postgres-depot")
@click.option('-n', 'depot_name', prompt=True, help="Name of the depot")
@click.option('-u', 'username', prompt=True, help="Username for the database")
@click.option('-p', 'password', prompt=True, hide_input=True, help="Password for the database")
@click.option('-h', 'hostname', prompt=True, help="Hostname of the database server")
@click.option('-d', 'database', prompt=True, help="Database name")
def create_postgres_depot(depot_name, username, password, hostname, database):
    """
    Create a YAML configuration for a PostgreSQL depot.
    """
    generator = ConfigGenerator(TEMPLATES_DIR)
    template_content = generator.load_template("depot/postgres.yaml")
    if template_content:
        config = generator.create_config(
            template_content,
            depot_name=depot_name,
            username=username,
            password=password,
            hostname=hostname,
            database=database
        )
        config_path = os.path.join(os.getcwd(), f"config-{depot_name}-depot.yaml")
        with open(config_path, 'w') as file:
            file.write(config)
        logging.info(f"Created depot configuration at {config_path}")


@click.command(name="create-snowflake-depot")
@click.option('-n', 'depot_name', prompt=True, help="Name of the depot")
@click.option('-u', 'username', prompt=True, help="Username for the database")
@click.option('-p', 'password', prompt=True, hide_input=True, help="Password for the database")
@click.option('-h', 'url', prompt=True, help="Hostname of the database server")
@click.option('-d', 'database', prompt=True, help="Database name")
@click.option('-w', 'warehouse', prompt=True, help="Warehouse name")
def create_snowflake_depot(depot_name, username, password, url, database,warehouse):
    """
    Create a YAML configuration for a PostgreSQL depot.
    """
    generator = ConfigGenerator(TEMPLATES_DIR)
    template_content = generator.load_template("depot/snowflakes.yaml")
    if template_content:
        config = generator.create_config(
            template_content,
            depot_name=depot_name,
            username=username,
            password=password,
            url=url,
            database=database,
            warehouse=warehouse
        )
        config_path = os.path.join(os.getcwd(), f"config-{depot_name}-depot.yaml")
        with open(config_path, 'w') as file:
            file.write(config)
        logging.info(f"Created depot configuration at {config_path}")

# Setup commands for different environments
setup_create_command('azure-postgres', 'postgres', 'public', 'flare/postgres/azure-postgres.yaml')
setup_create_command('postgres-icebase', 'icebase', 'default', 'flare/postgres/postgres-icebase.yaml')
setup_create_command('azure-bigquery', 'bigquery', 'default', 'flare/bigquery/azure-bigquery.yaml')
setup_create_command('bigquery-icebase', 'bigquery', 'default', 'flare/bigquery/bigquery-icebase.yaml')
cli.add_command(create_postgres_depot)
cli.add_command(create_snowflake_depot)

if __name__ == "__main__":
    cli()

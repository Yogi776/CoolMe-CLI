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
    Create a YAML configuration for a Snowflake depot.
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



@click.command(name="create-s3-depot")
@click.option('-depot_name', 'depot_name', prompt=True, help="Name of the depot")
@click.option('-bucket_name', 'bucket_name', prompt=True, help="Bucket Name for the S3")
@click.option('-relative_path', 'relative_path', prompt=True, hide_input=True, help="Relative path of the S3 Bucket")
@click.option('-access_key_id', 'access_key_id', prompt=True, help="Access key for the S3 Bucket")
@click.option('-access_secret_key_id', 'access_secret_key_id', prompt=True, help="Access secret key for the S3 Bucket")
def create_s3_depot(depot_name, bucket_name, relative_path, access_key_id, access_secret_key_id):
    """
    Create a YAML configuration for a S3 depot.

    Example usage:

        coolme create-s3-depot -depot_name poss3 -bucket_name tmdcsftptest -relative_path "/customer" -access_key_id <access_key_id> -access_secret_key_id <access_secret_key_id>
    """
    generator = ConfigGenerator(TEMPLATES_DIR)
    template_content = generator.load_template("depot/s3.yaml")
    if template_content:
        config = generator.create_config(
            template_content,
            depot_name=depot_name,
            bucket_name=bucket_name,
            relative_path=relative_path,
            access_key_id=access_key_id,
            access_secret_key_id=access_secret_key_id
        )
        config_path = os.path.join(os.getcwd(), f"config-{depot_name}-depot.yaml")
        with open(config_path, 'w') as file:
            file.write(config)
        logging.info(f"Created depot configuration at {config_path}")


@click.command(name="create-bigquery-depot")
@click.option('-depot_name', 'depot_name', prompt=True, help="Name of the depot")
@click.option('-project_id', 'project_id', prompt=True, help="Project ID of Bigquery")
@click.option('-json_keyfile', 'key_file', prompt=True, help="Path to JSON key file")
def create_bigquery_depot(depot_name, project_id, json_keyfile):
    """
    Create a YAML configuration for a Bigquery depot.

    Example usage:
    """
    generator = ConfigGenerator(TEMPLATES_DIR)
    template_content = generator.load_template("depot/bigquery.yaml")
    if template_content:
        config = generator.create_config(
            template_content,
            depot_name=depot_name,
            project_id=project_id,
            json_keyfile=json_keyfile
        )
        config_path = os.path.join(os.getcwd(), f"config-{depot_name}-depot.yaml")
        with open(config_path, 'w') as file:
            file.write(config)
        logging.info(f"Created depot configuration at {config_path}")


class FileOps:
    @staticmethod
    def create_directory(path):
        """Create a directory at the specified path if it does not exist."""
        try:
            os.makedirs(path, exist_ok=True)
            print(f"Created directory: {path}")
            return True
        except Exception as e:
            print(f"Failed to create directory {path}: {str(e)}")
            return False

    @staticmethod
    def create_file(path, content=""):
        """Create an empty file at the specified path only if it does not exist or is empty, and write content if provided."""
        if os.path.exists(path) and os.path.getsize(path) > 0:
            print(f"Skipped creating file as it already exists and is not empty: {path}")
            return False
        try:
            with open(path, 'w') as f:
                f.write(content)  # Write the provided content to the file
            print(f"Created file: {path}")
            return True
        except Exception as e:
            print(f"Failed to create file {path}: {str(e)}")
            return False

def generate_yaml_content(entity):
    """Generate YAML content based on a template and the specified entity."""
    return (
        f"tables:\n"
        f"  - name: {entity}\n"
        f"    sql:  {{{{ load_sql('{entity}') }}}}\n"
        f"    description: \"This table captures detailed data about {entity}.\"\n"
        f"    data_source: icebase\n"
        f"    public: true\n"
        f"    joins:\n"
        f"      - name: tables\n"
        f"        relationship: one_to_one\n"
        f"        sql: \"{{ TABLE.key }}= {{ tables.key }}\" \n"
        f"    dimensions:\n"
        f"      - name: id\n"
        f"        description: \"Unique identifier for each {entity}, linking it to related activities.\"\n"
        f"        type: number\n"
        f"        column: id\n"
        f"        primary_key: true\n"
        f"        public: true\n"
    )



@click.command(name="create-lens")
@click.option('-n', '--name', prompt="Enter the base directory name", help="Name of the base directory")
@click.option('-e', '--entities', prompt="Enter entities separated by commas", help="List of entities, separated by commas")
def create_lens(name, entities):
    """
    This command creates directories and files for specified entities in a structured project directory.
    """
    entities = [entity.strip() for entity in entities.split(",")]

    base_dir = name
    sql_dir = os.path.join(base_dir, "model/sqls")
    table_dir = os.path.join(base_dir, "model/tables")
    model_dir = os.path.join(base_dir, "model")  # General model directory

    # Create directories using ops
    if FileOps.create_directory(sql_dir) and FileOps.create_directory(table_dir) and FileOps.create_directory(model_dir):
        for entity in entities:
            sql_file_path = os.path.join(sql_dir, f"{entity}.sql")
            yaml_content = generate_yaml_content(entity)
            yaml_file_path = os.path.join(table_dir, f"{entity}.yaml")

            # Create SQL and YAML files using ops
            FileOps.create_file(sql_file_path)
            FileOps.create_file(yaml_file_path, yaml_content)

        # Create files that do not depend on entities
        user_group_file_path = os.path.join(model_dir, "user_group.yml")
        deployment_file_path = os.path.join(base_dir, "deployment.yaml")
        FileOps.create_file(user_group_file_path)  # Create once, not per entity
        FileOps.create_file(deployment_file_path)  # Create once, not per entity


# Setup commands for different environments
setup_create_command('azure-postgres', 'postgres', 'public', 'flare/postgres/azure-postgres.yaml')
setup_create_command('postgres-icebase', 'icebase', 'default', 'flare/postgres/postgres-icebase.yaml')
setup_create_command('azure-bigquery', 'bigquery', 'default', 'flare/bigquery/azure-bigquery.yaml')
setup_create_command('bigquery-icebase', 'bigquery', 'default', 'flare/bigquery/bigquery-icebase.yaml')

cli.add_command(create_postgres_depot)
cli.add_command(create_snowflake_depot)
cli.add_command(create_s3_depot)
cli.add_command(create_bigquery_depot)
cli.add_command(create_lens)

if __name__ == "__main__":
    cli()

import os

def create_directory(path):
    """Create a directory at the specified path if it does not exist."""
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Created directory: {path}")
    except Exception as e:
        print(f"Failed to create directory {path}: {str(e)}")

def create_file(path, content=""):
    """Create an empty file at the specified path only if it does not exist or is empty, and write content if provided."""
    if os.path.exists(path) and os.path.getsize(path) > 0:
        print(f"Skipped creating file as it already exists and is not empty: {path}")
    else:
        try:
            with open(path, 'w') as f:
                f.write(content)  # Write the provided content to the file
            print(f"Created file: {path}")
        except Exception as e:
            print(f"Failed to create file {path}: {str(e)}")


def generate_yaml_content(entity):
    """Generate YAML content based on a template and the specified entity."""
    raw_start = "{% raw %}"
    raw_end = "{% endraw %}"
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



def main():
    base_dir = "Jeweler360"
    entities = ["customer", "product", "order"]

    # Directories where files will be created
    sql_dir = os.path.join(base_dir, "model/sqls")
    table_dir = os.path.join(base_dir, "model/tables")
    model_dir = os.path.join(base_dir, "model")  # Added for general model files

    # Ensure directories exist
    create_directory(sql_dir)
    create_directory(table_dir)
    create_directory(model_dir)  # Ensure the model directory exists

    # Create files for each entity in the respective directories
    for entity in entities:
        sql_file_path = os.path.join(sql_dir, f"{entity}.sql")
        yaml_content = generate_yaml_content(entity)
        print(yaml_content)
        yaml_file_path = os.path.join(table_dir, f"{entity}.yaml")

        create_file(sql_file_path)  # Create empty SQL file
        create_file(yaml_file_path, yaml_content)  # Create YAML file with dynamic content

    # Create the user_group.yml file in the model directory
    user_group_file_path = os.path.join(model_dir, "user_group.yml")
    create_file(user_group_file_path)

if __name__ == "__main__":
    main()

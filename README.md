
# CoolMe CLI Tool

CoolMe is a command-line interface tool designed to automate the generation of workflow and policy YAML files for data ingestion processes. It supports custom configurations for different ingestion types and allows users to specify input and output settings for data processing tasks.

## Prerequisites

Before you install and run CoolMe, ensure you have the following installed:
- Python 3.6 or higher
- Conda (if you prefer using Conda environments)
- pip (Python package installer)

## Installation

### Using Conda

If you prefer to use Conda, you can create and activate a Conda environment specifically for CoolMe:

1. Create a Conda environment:
   ```bash
   conda create -n coolme python=3.11
   ```

2. Activate the environment:
   ```bash
   conda activate coolme
   ```

### Using Pip and Virtual Environments

To install CoolMe using pip in a virtual environment:

1. Clone the repository or download the source code:
   ```bash
   git clone git@github.com:Yogi776/CoolMe-CLI.git
   cd CoolMe-CLI
   ```
### Using Pip and Virtual Environments

To install CoolMe using pip in a virtual environment:

1. Clone the repository or download the source code:
   ```bash
   git clone git@github.com:Yogi776/CoolMe-CLI.git
   cd CoolMe-CLI
   ```

2. If not using Conda, set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
   ```

3. Install the package using pip:
   ```bash
   make install
   ```

This will install all required dependencies and allow you to run the `coolme` command directly from the command line.

## Usage

### Running Commands with Makefile

For ease of use and to streamline workflow execution, the following Make commands are available:

- **postgres-icebase**: Configure a single customer item for Postgres-Icebase.
  ```bash
  make postgres-icebase
  ```

- **azure-postgres**: Configure a single product item for Azure PostgreSQL.
  ```bash
  make azure-postgres
  ```
  
Here are the available Makefile commands for setting up different environments:

| Command           | Description                              | Usage Example                                               |
|-------------------|------------------------------------------|-------------------------------------------------------------|
| `azure-postgres`  | Configures items for Azure PostgreSQL.   | `make azure-postgres`                                       |
| `postgres-icebase`| Configures items for Postgres-Icebase.   | `make postgres-icebase`                                     |
| `azure-bigquery`  | Configures items for Azure BigQuery.     | `make azure-bigquery`                                       |
| `bigquery-icebase`| Configures items for BigQuery-Icebase.   | `make bigquery-icebase`                                     |

### Detailed Command Usage

Commands for custom configurations can be run with detailed parameters:

```bash
coolme create-<environment> \
    --project_name <name> \
    --data-product <product> \
    --entity "<entities>" \
    --output-catalog <catalog> \
    --output-schema <schema> \
    --output-tables "<table mappings>" \
    --template-path "<path>"
```

#### Example Commands

| Environment       | Command                                                                 |
|-------------------|-------------------------------------------------------------------------|
| Azure PostgreSQL  | `coolme create-azure-postgres --project_name jeweler360 --data-product customer --entity "product,service,order" --output-catalog icebase --output-schema sandbox --output-tables "product=product_data,service=service_data,order=order_data"` |
| Postgres Icebase  | `coolme create-postgres-icebase --project_name jeweler360 --data-product customer --output-schema sandbox --output-tables "customer=customer_table"` |
| Azure BigQuery    | `coolme create-azure-bigquery --project_name jeweler360 --data-product customer --entity "product,service,order" --output-catalog icebase --output-schema sandbox --output-tables "product=product_data,service=service_data,order=order_data"` |
| BigQuery Icebase  | `coolme create-bigquery-icebase --project_name jeweler360 --data-product customer --output-schema sandbox --output-tables "customer=customer_table"` |


To use CoolMe for custom configurations, run commands in the following format:
```bash
coolme create-azure-postgres \
    --project_name jeweler360 \
    --data-product customer \
    --entity "product,service,order" \
    --output-catalog icebase \
    --output-schema sandbox \
    --output-tables "product=product_data,service=service_data,order=order_data" \
    --template-path "/path/to/azure-postgres.yaml"
```

#### Examples

- **Multiple Item Configuration**:
  ```bash
  coolme create-azure-postgres --project_name jeweler360 --data-product customer 	--entity "product,service,order" 	--output-catalog icebase 	--output-schema sandbox	--output-tables "product=product_data,service=service_data,order=order_data"
  ```

- **Single Item Configuration**:
  ```bash
  coolme create-postgres-icebase  --project_name jeweler360 --data-product customer  --output-schema sandbox --output-tables "customer=customer_table"
  ```

---
## Command: `create-postgres-depot`

This command creates a configuration file for a PostgreSQL depot based on user-provided parameters.

### Usage

Run the command using Makefile:

```bash
make create-postgres-depot
```

Alternatively, execute the command directly (assuming `coolme` is set up correctly):

```bash
coolme create-postgres-depot -n your_depot_name -u your_username -p your_password -h your_hostname -d your_database
```

### Parameters

The table below lists and describes each parameter used with the `create-postgres-depot` command:

| Parameter | Flag | Description                                           | Required |
|-----------|------|-------------------------------------------------------|:--------:|
| Name      | `-n` | The name of the depot to be created.                  | Yes      |
| Username  | `-u` | The username required for database access.            | Yes      |
| Password  | `-p` | The password for database access.                     | Yes      |
| Hostname  | `-h` | The hostname of the PostgreSQL server.                | Yes      |
| Database  | `-d` | The name of the database to connect to.               | Yes      |

### Example

Here is an example command that illustrates how to use `create-postgres-depot` with all parameters filled in:

```bash
coolme create-postgres-depot -n postgres -u postgres -p 12345 -h sandbox.postgres.database.azure.com -d postgres

```
---

## Command: `create-snowflake-depot`
```bash
make create-snowflake-depot
```

Alternatively, execute the command directly (assuming `coolme` is set up correctly):

```bash
coolme create-snowflake-depot -n depot_name -u username -p password -h hostname -d databasename -w warehouse
```

### Parameters

The table below lists and describes each parameter used with the `create-snowflake-depot` command:

| Parameter | Flag | Description                                           | Required |
|-----------|------|-------------------------------------------------------|:--------:|
| Name      | `-n` | The name of the depot to be created.                  | Yes      |
| Username  | `-u` | The username required for database access.            | Yes      |
| Password  | `-p` | The password for database access.                     | Yes      |
| Hostname  | `-h` | The hostname of the Snowflake server.                 | Yes      |
| Database  | `-d` | The name of the database to connect to.               | Yes      |
| Warehouse | `-w` | The name of the Snowflake warehouse to be used.       | Yes      |

### Example

Here is an example command that illustrates how to use `create-snowflake-depot` with all parameters filled in:

```bash
coolme create-snowflake-depot -n snowflake -u yash -p Pk.99@1234 -h WIIHBDA-PF56723.snowflakecomputing.com -d SNOWFLAKE_SAMPLE_DATA -w COMPUTE_WH
```
This command will create a new Snowflake depot named `snowflake` with the specified access credentials and database details.

---

## Command: `create-lens`
```bash
make create-lens
```

Alternatively, execute the command directly (assuming `coolme` is set up correctly):

```bash
coolme create-lens -n lens_name -e "entity1,entity2,entity3"
```

### Parameters

The table below lists and describes each parameter used with the `create-lens` command:

| Parameter | Flag | Description                                                | Required |
|-----------|------|------------------------------------------------------------|:--------:|
| Name      | `-n` | The name of the lens to be created.                        | Yes      |
| Entities  | `-e` | A comma-separated list of entities to include in the lens. | Yes      |

### Example

Here is an example command that illustrates how to use `create-lens` with all parameters filled in:

```bash
coolme create-lens -n customer-360 -e "customer,product,order,transaction,city,order-data"
```

---
## Contributing

Contributions to CoolMe are welcome! Please ensure you follow the contributing guidelines in the CONTRIBUTING.md file.

vide all necessary information for both beginning users and developers, ensuring that anyone can get started quickly and understand how to use the tool effectively.
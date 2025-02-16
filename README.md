
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

- **postgres-icebase-all**: Configure multiple items for Postgres-Icebase environment.
  ```bash
  make postgres-icebase-all
  ```

- **postgres-icebase**: Configure a single customer item for Postgres-Icebase.
  ```bash
  make postgres-icebase
  ```

- **azure-postgres**: Configure a single product item for Azure PostgreSQL.
  ```bash
  make azure-postgres
  ```

- **azure-postgres-all**: Configure multiple items for Azure PostgreSQL environment.
  ```bash
  make azure-postgres-all
  ```

These commands abstract complex CLI commands into simple Make commands that execute predefined configurations.

### Custom Command Execution

To use CoolMe for custom configurations, run commands in the following format:
```bash
coolme create azure-postgres \
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
  coolme create azure-postgres --project_name jeweler360 --data-product customer 	--entity "product,service,order" 	--output-catalog icebase 	--output-schema sandbox	--output-tables "product=product_data,service=service_data,order=order_data"
  ```

- **Single Item Configuration**:
  ```bash
  coolme create postgres-icebase  --project_name jeweler360 --data-product customer  --output-schema sandbox --output-tables "customer=customer_table"
  ```
## Contributing

Contributions to CoolMe are welcome! Please ensure you follow the contributing guidelines in the CONTRIBUTING.md file.

vide all necessary information for both beginning users and developers, ensuring that anyone can get started quickly and understand how to use the tool effectively.
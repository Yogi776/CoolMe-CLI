
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

To use CoolMe, you need to run commands in the following format:
```bash
coolme create [project_name] [ingestion_items...] --type [ingestion_type] --output-catalog [catalog_name] --output-schema [schema_name] --output-tables "[item1=table1,item2=table2,...]"
```

### Command Arguments and Options

- `project_name`: The name of your project.
- `ingestion_items`: A space-separated list of items that you want to configure for ingestion.
- `--type`: Specifies the type of ingestion process (default: "default"). Examples include "default" and "postgres-icebase".
- `--output-catalog`: The name of the output catalog.
- `--output-schema`: The name of the output schema.
- `--output-tables`: A comma-separated mapping of ingestion items to their respective output tables. Format: "item1=table1,item2=table2".

### Examples

#### Multiple Item Configuration
Here is an example command that uses the CoolMe tool to create configurations for the `jeweler360` project with multiple ingestion items:
```bash
coolme create jeweler360 customer product inventory --type postgres-icebase --output-catalog icebase --output-schema sandbox --output-tables "customer=customer_table,product=product_table,inventory=inventory_table"
```
This command will create YAML files for `customer`, `product`, and `inventory` in the specified directory based on the `postgres-icebase` template with specified output settings.

#### Single Item Configuration
For simpler use cases or testing single data ingestion configurations, you can execute a command for just one item. For example:
```bash
coolme create jeweler360 customer --type postgres-icebase --output-catalog icebase --output-schema sandbox --output-tables "customer=customer_table"
```
This command specifically creates a configuration for only the `customer` item, making it ideal for focused tasks or initial testing phases.

## Contributing

Contributions to CoolMe are welcome! Please ensure you follow the contributing guidelines in the CONTRIBUTING.md file.

## License

CoolMe is released under the MIT License. See the LICENSE file for more details.

---

### Additional Notes

- **Support and Contact Information**: Include contact info or links to issue trackers if users need support or want to report bugs.
- **Detailed Documentation**: Consider linking to more detailed documentation if your tool is complex or has many features.

This README is structured to provide all necessary information for both beginning users and developers, ensuring that anyone can get started quickly and understand how to use the tool effectively.
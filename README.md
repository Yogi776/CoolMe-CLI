
# CoolMe CLI Tool

CoolMe is a command-line interface tool designed to automate the generation of workflow and policy YAML files for data ingestion processes. It supports custom configurations for different ingestion types and allows users to specify input and output settings for data processing tasks.

## Prerequisites

Before you install and run CoolMe, ensure you have the following installed:
- Python 3.6 or higher
- pip (Python package installer)

## Installation

To install CoolMe, follow these steps:

1. Clone the repository or download the source code:
   ```bash
   git clone git@github.com:Yogi776/CoolMe-CLI.git
   cd CoolMe-CLI
   ```

2. Install the package using pip:
   ```bash
   pip install -e .
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
- `--type`: Specifies the type of ingestion process (default: "default"). Example: "postgres-icebase".
- `--output-catalog`: The name of the output catalog.
- `--output-schema`: The name of the output schema.
- `--output-tables`: A comma-separated mapping of ingestion items to their respective output tables. Format: "item1=table1,item2=table2".

### Example

Here is an example command that uses the CoolMe tool to create configurations for the `jeweler360` project with multiple ingestion items:

```bash
coolme create jeweler360 customer product inventory --type postgres-icebase --output-catalog icebase --output-schema sandbox --output-tables "customer=customer_table,product=product_table,inventory=inventory_table"
```

This command will create YAML files for `customer`, `product`, and `inventory` in the `jeweler360/customer/build/data-processing` directory based on the `postgres-icebase` template with specified output settings.

### Sample Single File Creation
```bash
coolme create jeweler360 customer --type postgres-icebase --output-catalog icebase --output-schema sandbox --output-tables "customer=customer_table"
```
## Contributing

Contributions to CoolMe are welcome! Please ensure you follow the contributing guidelines in the CONTRIBUTING.md file.

## License

CoolMe is released under the MIT License. See the LICENSE file for more details.

---

### Additional Notes

- **Customization**: Customize the README with any specific configuration or environment variables that are relevant to your tool.
- **Support and Contact Information**: Include contact info or links to issue trackers if users need support or want to report bugs.
- **Detailed Documentation**: Consider linking to more detailed documentation if your tool is complex or has many features.

This template should give you a strong starting point for documenting your CLI tool and helping users get started with it effectively.
.PHONY: install clean test run

# Install the package in editable mode
install:
	pip install -e .

# Run the coolme create command with predefined parameters
postgres-icebase-all:
	coolme create-postgres-icebase jeweler360 customer customer product inventory order \
	--output-catalog icebase \
	--output-schema sandbox \
	--output-tables "customer=customer_table,product=product_table,inventory=inventory_table,order=order_table"


postgres-icebase:
	coolme create-postgres-icebase jeweler360 customer  customer \
	--output-catalog icebase \
	--output-schema sandbox \
	--output-tables "customer=customer_table"


azure-postgres:
	coolme create-azure-postgres jeweler360 customer product \
	--output-catalog icebase \
	--output-schema sandbox \
	--output-tables "product=product_data"


azure-postgres-all:
	coolme create azure-postgres jeweler360 customer customer product inventory order \
	--output-catalog icebase \
	--output-schema sandbox \
	--output-tables "customer=customer_table,product=product_table,inventory=inventory_table,order=order_table"


test:
	coolme create-postgres-icebase --project_name jeweler360 --data-product customer \
		--entity "product,service,order" \
		--output-catalog icebase \
		--output-schema sandbox \
		--output-tables "product=product_data,service=service_data,order=order_data"


test-dev:
	coolme create-azure-bigquery \
		--project_name jeweler360 \
		--data-product customer \
		--entity "product,service,order" \
		--output-catalog icebase \
		--output-schema sandbox \
		--output-tables "product=product_data,service=service_data,order=order_data"


create-postgres-depot:
	@coolme create-postgres-depot -n postgres -u postgres -p 12345 -h sandbox.postgres.database.azure.com -d postgres


create-snowflake-depot:
	@coolme create-snowflake-depot -n snowflake -u yash -p Pk.99@1234 -h WIIHBDA-PF56723.snowflakecomputing.com -d SNOWFLAKE_SAMPLE_DATA -w COMPUTE_WH
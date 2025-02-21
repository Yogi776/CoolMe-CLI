.PHONY: install clean test run

# Install the package in editable mode
install:
	pip install -e .

# Run the coolme create command with predefined parameters
postgres-icebase-all:
	coolme create-postgres-icebase --project_name jeweler360 --data-product customer \
	--entity "customer,product,inventory,order" \
	--output-catalog icebase \
	--output-schema sandbox \
	--output-tables "customer=customer_table,product=product_table,inventory=inventory_table,order=order_table"


postgres-icebase:
	coolme create-postgres-icebase --project_name jeweler360 --data-product customer \
	--entity "customer" \
	--output-catalog icebase \
	--output-schema sandbox \
	--output-tables "customer=customer_table"


azure-postgres:
	coolme create-azure-postgres --project_name jeweler360 --data-product customer \
	--entity "product" \
	--output-catalog icebase \
	--output-schema sandbox \
	--output-tables "product=product_data"


azure-postgres-all:
	coolme create azure-postgres --project_name jeweler360 --data-product customer \
 	--entity "customer,product,inventory,order" \
	--output-catalog icebase \
	--output-schema sandbox \
	--output-tables "customer=customer_table,product=product_table,inventory=inventory_table,order=order_table"


test:
	coolme create-postgres-icebase --project_name jeweler360 --data-product customer \
		--entity "product,order" \
		--output-catalog icebase \
		--output-schema sandbox \
		--output-tables "product=product_data,order=order_data"


test-dev:
	coolme create-azure-bigquery \
		--project_name jeweler360 \
		--data-product customer \
		--entity "product,service,order" \
		--output-catalog postgres \
		--output-schema sandbox \
		--output-tables "product=product_data,service=service_data,order=order_data"


create-postgres-depot:
	@coolme create-postgres-depot -n postgres -u postgres -p 12345 -h sandbox.postgres.database.azure.com -d postgres


create-snowflake-depot:
	@coolme create-snowflake-depot -n snowflake -u yash -p Pk.99@1234 -h WIIHBDA-PF56723.snowflakecomputing.com -d SNOWFLAKE_SAMPLE_DATA -w COMPUTE_WH



create-s3-depot:
	@coolme create-s3-depot -depot_name poss3 -bucket_name tmdcsftptest -relative_path "/customer" -access_key_id <access_key_id> -access_secret_key_id <access_secret_key_id>

create-lens:
	@coolme create-lens -n customer-360 -e "customer,product,order,transaction,city,order-data"
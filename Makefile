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
	coolme create-azure-postgres \
		--project_name jeweler360 \
		--data-product customer \
		--entity "product,service,order" \
		--output-catalog icebase \
		--output-schema sandbox \
		--output-tables "product=product_data,service=service_data,order=order_data"

# 	coolme create azure-postgres --project_name jeweler360 --data-product customer 	--entity "product,service,order" 	--output-catalog icebase 	--output-schema sandbox	--output-tables "product=product_data,service=service_data,order=order_data"
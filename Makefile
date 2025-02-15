.PHONY: install clean test run

# Install the package in editable mode
install:
	pip install -e .

# Run the coolme create command with predefined parameters
run:
	coolme create workflow jeweler360 customer product inventory order \
	--type postgres-icebase \
	--output-catalog icebase \
	--output-schema sandbox \
	--output-tables "customer=customer_table,product=product_table,inventory=inventory_table,order=order_table"


tables:
	coolme create workflow jeweler360 customer \
	--type postgres-icebase \
	--output-catalog icebase \
	--output-schema sandbox \
	--output-tables "customer=customer_table"
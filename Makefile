.PHONY: install clean test run

# Install the package in editable mode
install:
	pip install -e .

# Run the coolme create command with predefined parameters
postgres-icebase-all:
	coolme create postgres-icebase customer jeweler360 customer product inventory order \
	--output-catalog icebase \
	--output-schema sandbox \
	--output-tables "customer=customer_table,product=product_table,inventory=inventory_table,order=order_table"


postgres-icebase:
	coolme create postgres-icebase customer jeweler360 customer \
	--output-catalog icebase \
	--output-schema sandbox \
	--output-tables "customer=customer_table"


azure-postgres:
	coolme create azure-postgres product jeweler360 product \
	--output-catalog icebase \
	--output-schema sandbox \
	--output-tables "product=product_data"


azure-postgres-all:
	coolme create azure-postgres customer jeweler360 customer product inventory order \
	--output-catalog icebase \
	--output-schema sandbox \
	--output-tables "customer=customer_table,product=product_table,inventory=inventory_table,order=order_table"

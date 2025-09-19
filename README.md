# iteso-bdnr-cassandra-logistics

Logistics system with Cassandra for handling orders, products, and shipments.

## System Description

This system manages a complete logistics flow that includes:
- **Customers**: Contact information of buyers
- **Orders**: Requests made by customers  
- **Products**: Items included in each order
- **Shipments**: Package and delivery tracking

## Data Model

The system implements the following optimized queries:

### Q1: `orders_by_customers`
- **Query**: Get all orders from a customer ordered by date

### Q2: `products_by_order` 
- **Query**: Get all products from an order ordered by price

### Q3: Shipment Queries (`shipments_by_*`)
Multiple tables for different shipment query patterns:

- **Q3.1 & Q3.2**: `shipments_by_o_sd` - Shipments by order and date
- **Q3.3**: `shipments_by_o_ssd` - Shipments by order, status and date
- **Q3.4**: `shipments_by_o_tsd` - Shipments by order, type and date  
- **Q3.5**: `shipments_by_o_tssd` - Shipments by order, type, status and date

## Sample Data
The system includes sample data with:
- 6 customers
- 15 diverse products
- Order statuses
- Shipment statuses
- Shipment types

## Environment Setup

### Configure Python virtual environment
```bash
# If pip is not present in your system
sudo apt update
sudo apt install python3-pip

# Install and activate virtual env (Linux/MacOS)
python3 -m pip install virtualenv
python3 -m venv ./venv
source ./venv/bin/activate

# Install and activate virtual env (Windows)
python3 -m pip install virtualenv
python3 -m venv ./venv
.\venv\Scripts\Activate.ps1

# Install project dependencies
pip install -r requirements.txt

# To start a new container
docker run --name logistics -p 9042:9042 -d cassandra

# If the container already exists, just start it
docker start logistics

# Run the app
python3 app.py
```
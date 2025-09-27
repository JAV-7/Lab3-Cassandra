#!/usr/bin/env python3
import logging
import os

from cassandra.cluster import Cluster

import model

# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('logistics.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to Cassandra App
CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', '127.0.0.1')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'logistics')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')

def print_menu():
    mm_options = {
        0: "Populate sample data",
        1: "Show orders by customer (Q1)",
        2: "Show products by order (Q2)",
        3: "Show all shipments by order (Q3.1)",
        4: "Show shipments by order with date range (Q3.2)",
        5: "Show shipments by order and status with date range (Q3.3)",
        6: "Show shipments by order and type with date range (Q3.4)",
        7: "Show shipments by order, type and status with date range (Q3.5)",
        8: "Change working email",
        9: "Exit",
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])

def set_customer_email():
    print("\nSample customer emails:")
    for email, name, _, _ in model.CUSTOMERS:
        print(f"  - {email} ({name})")
    
    email = input('\n**** Customer email to use: ').strip()
    log.info(f"Customer email set to {email}")
    return email

def get_order_number():
    order_number = input('Enter order number: ').strip()
    return order_number

def get_shipment_status():
    print(f"\nAvailable statuses: {', '.join(model.SHIPMENT_STATUSES)}")
    while True:
        status = input('Enter shipment status: ').strip()
        if status in model.SHIPMENT_STATUSES:
            return status
        print("Invalid status, please choose exactly one from the list.")

def get_shipment_type():
    print(f"\nAvailable types: {', '.join(model.SHIPMENT_TYPES)}")
    while True:
        ship_type = input('Enter shipment type: ').strip()
        if ship_type in model.SHIPMENT_TYPES:
            return ship_type
        print("Invalid status, please choose exactly one from the list.")

def main():
    log.info("Connecting to Cluster")
    cluster = Cluster(CLUSTER_IPS.split(','))
    session = cluster.connect()

    model.create_keyspace(session, KEYSPACE, REPLICATION_FACTOR)
    session.set_keyspace(KEYSPACE)

    model.create_schema(session)

    customer_email = set_customer_email()

    # HW
    while(True):
        print("\n" + "="*50)
        print_menu()
        try:
            option = int(input('\nEnter your choice: '))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if option == 0:
            print("Populating sample data...")
            model.bulk_insert(session)
            print("Sample data populated successfully!")

        elif option == 1:
            print(f"\nQ1: Getting orders for customer: {customer_email}")
            model.get_orders_by_customer(session, customer_email)

        elif option == 2:
            order_number = get_order_number()
            print(f"\nQ2: Getting products by order: {order_number}")
            model.get_products_by_order(session, order_number)

        elif option == 3:
            order_number = get_order_number()
            print(f"\nQ3.1: Getting all shipments by order: {order_number}")
            model.get_shipments_by_order(session, order_number)

        elif option == 4:
            order_number = get_order_number()
            print(f"\nQ3.2: Getting shipments by order with date range: {order_number}")
            start_date = input('Enter start date (YYYY-MM-DD): ').strip()
            end_date = input('Enter end date (YYYY-MM-DD): ').strip()
            model.get_shipments_by_order_date_range(session, order_number, start_date, end_date)

        elif option == 5:
            order_number = get_order_number()
            status = get_shipment_status()
            print(f"\nQ3.3: Getting shipments by order and status with date range: {order_number}, {status}")
            start_date = input('Enter start date (YYYY-MM-DD): ').strip()
            end_date = input('Enter end date (YYYY-MM-DD): ').strip()
            model.get_shipments_by_order_status_date_range(session, order_number, status, start_date, end_date) 

        elif option == 6:
            order_number = get_order_number()
            ship_type = get_shipment_type()
            print(f"\nQ3.4: Getting shipments by order and type with date range: {order_number}, {ship_type}")
            start_date = input('Enter start date (YYYY-MM-DD): ').strip()
            end_date = input('Enter end date (YYYY-MM-DD): ').strip()
            model.get_shipments_by_order_type_date_range(session, order_number, ship_type, start_date, end_date)

        elif option == 7:
            order_number = get_order_number()
            ship_type = get_shipment_type()
            status = get_shipment_status()
            print(f"\nQ3.5: Getting shipments by order, type and status with date range: {order_number}, {ship_type}, {status}")
            start_date = input('Enter start date (YYYY-MM-DD): ').strip()
            end_date = input('Enter end date (YYYY-MM-DD): ').strip()
            model.get_shipments_by_order_type_status_date_range(session, order_number, ship_type, status, start_date, end_date)

        elif option == 8:
            customer_email = set_customer_email()

        elif option == 9:
            print("Exiting logistics application...")
            exit(0)

        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()
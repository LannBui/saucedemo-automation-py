import csv
import os

def get_login_data_from_csv(file_path):
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', file_path))
    with open(abs_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [(row['username'], row['password'], row.get('expected_error', '')) for row in reader]

def get_checkout_data_from_csv(file_path):
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', file_path))
    with open(abs_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [(row['first_name'], row['last_name'], row['postal_code'], row.get('expected_error','')) for row in reader]

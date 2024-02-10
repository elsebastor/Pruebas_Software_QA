"""
This module contains functions for processing data using sys, and collections.
"""
import sys
import json
import time as t
import pandas as pd


def read_product_list(file_path):
    """
    reads the product list and validate
    """
    try:
        with open(file_path, 'r', encoding='UTF-8') as file:
            data = json.load(file)

        # Check if data is a list of dictionaries
        if not isinstance(data, list)\
           or not all(isinstance(item, dict) for item in data):
            print("Error: JSON data is not a list of dictionaries.")
            return pd.DataFrame()

        expected_types = {
            "title": str,
            "type": str,
            "description": str,
            "filename": str,
            "height": int,
            "width": int,
            "price": float,
            "rating": int
        }

        def log_error(key, expected, actual):
            print(f"'{key}' has type.{expected}, got {type(actual).__name__}.")

        def is_incorrect(key, data_point):
            expected_type = expected_types.get(key, None)
            if not isinstance(data_point, expected_type) and expected_type:
                log_error(key, expected_type.__name__, data_point)
                return True
            return False

        def correct_data(item):
            corrected = {}
            for key, value in item.items():
                if key in expected_types:
                    corrected[key] = None if is_incorrect(key, value) \
                          else value
            return corrected

        corrected_data = [correct_data(item) for item in data]

        # Convert the list of corrected dictionaries into a pandas DataFrame
        df = pd.DataFrame(corrected_data)
        return df

    except IOError as e:
        print(f"An IO error occurred: {e}")
        return pd.DataFrame()


def read_sales(file_path):
    """
    reads the sales list and validate
    """
    try:
        with open(file_path, 'r', encoding='UTF-8') as file:
            data = json.load(file)

        # Check if data is a list of dictionaries
        if not isinstance(data, list)\
           or not all(isinstance(item, dict) for item in data):
            print("Error: JSON data is not a list of dictionaries.")
            return pd.DataFrame()

        expected_types = {
            "SALE_ID": int,
            "SALE_Date": str,
            "Product": str,
            "Quantity": int
        }

        def log_error(key, expected, actual):
            print(f"Error: Key '{key}' has incorrect type. Expected \
                  {expected}, got {type(actual).__name__}.")

        def is_incorrect(key, data_point):
            expected_type = expected_types.get(key, None)
            if not isinstance(data_point, expected_type) and expected_type:
                log_error(key, expected_type.__name__, data_point)
                return True
            return False

        def correct_data(item):
            corr = {}
            for key, value in item.items():
                if key in expected_types:
                    corr[key] = None if is_incorrect(key, value) else value
            return corr

        corrected_data = [correct_data(item) for item in data]

        # Convert the list of corrected dictionaries into a pandas DataFrame
        df = pd.DataFrame(corrected_data)
        return df

    except IOError as e:
        print(f"An IO error occurred: {e}")
        return pd.DataFrame()


def compute_total_cost(product_catalog, sales_records):
    """ The program shall compute the total cost
        for all sales included in the second JSON archive.
        The total cost should include all items in the sale
        considering the cost for every item in the first file."""
    # Join the product catalog and sales
    joined_df = product_catalog.merge(sales_records,
                                      left_on='title',
                                      right_on='Product',
                                      how='inner')
    # Compute the total cost of each sale
    joined_df['total_cost'] = joined_df['price'] * joined_df['Quantity']
    # Group by product and sum the total cost
    total_cost_product = joined_df.groupby('Product')['total_cost'].sum()
    # Convert the result to a dataframe
    total_cost_df = total_cost_product.reset_index()
    # sum total cost
    total = total_cost_df['total_cost'].sum()

    return total


def write_to_txt_file(total_cost, elapsed, output_file_path):
    """Writes the total cost to a text file."""
    try:
        with open(output_file_path, 'w', encoding='UTF-8') as file:
            # write the elapsed time to the file
            file.write(f"Elapsed time: {elapsed}\n")
            # write the total cost to the file
            file.write(f"total cost: {total_cost}")
    except FileNotFoundError:
        print(f"File not found: {output_file_path}")
        sys.exit(1)


def print_total_cost(total_cost, elapsed):
    """Prints the total cost to the console."""
    print(f"Elapsed time: {elapsed}")
    print(f"Total Cost: {total_cost}")
    # print the elapsed time


def main(catalog_file_path, sales_file_path):
    """
    main function
    """
    start = t.time()
    try:
        catalog = read_product_list(catalog_file_path)
        sales = read_sales(sales_file_path)

        total_cost = compute_total_cost(catalog, sales)
    except IOError as e:
        print(f"An IO error occurred: {e}")
        sys.exit(1)
    end = t.time()
    elapsed = end - start
    write_to_txt_file(total_cost, elapsed, 'SalesResults.txt')
    print_total_cost(total_cost, elapsed)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <catalog_file_path> <sales_file_path>")
        sys.exit(1)
    catalog_file_path_v = sys.argv[1]
    sales_file_path_v = sys.argv[2]
    main(catalog_file_path_v, sales_file_path_v)

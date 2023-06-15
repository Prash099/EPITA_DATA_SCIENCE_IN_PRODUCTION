import csv
import pandas as pd
import os
import datetime
from great_expectations.dataset import PandasDataset
from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.core.expectation_configuration import ExpectationConfiguration
from Py_Scripts.save_data_logs import save_data_logs
from Py_Scripts.db_engine import db_engine
from Py_Scripts import input_file_great_expectations, output_directory_great_expectations, value_ranges


def split_csv_files(file_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    base_filename = datetime.datetime.now().strftime("%Y%m%d")
    output_files = []

    for root, _, files in os.walk(file_path):
        for filename in files:
            if filename.endswith('.csv'):
                csv_file_path = os.path.join(root, filename)

                with open(csv_file_path, 'r') as file:
                    reader = csv.reader(file)
                    header = next(reader)
                    rows = list(reader)

                # If the number of rows is less than or equal to 500, save the file directly
                if len(rows) <= 500:
                    output_file_path = os.path.join(output_folder, filename)
                    output_files.append(output_file_path)

                    with open(output_file_path, 'w', newline='') as output_file:
                        writer = csv.writer(output_file)
                        writer.writerow(header)
                        writer.writerows(rows)
                else:
                    for i in range(0, len(rows), 500):
                        filename_without_extension = os.path.splitext(filename)[0]
                        output_file_path = os.path.join(output_folder, f"{base_filename}_{filename_without_extension}_{i // 500 + 1}.csv")
                        output_files.append(output_file_path)

                        with open(output_file_path, 'w', newline='') as output_file:
                            writer = csv.writer(output_file)
                            writer.writerow(header)
                            writer.writerows(rows[i:i+500])

    return output_files


def validate_csv_files(session, file_folder):
    suite = create_expectation_suite(value_ranges)
    for file_name in os.listdir(file_folder):
        file_path = os.path.join(file_folder, file_name)
        errors = []  # Initialize errors list for each file
        df = pd.read_csv(file_path)  # Read the entire DataFrame for the file

        for row_number, row in df.iterrows():  # Iterate over rows of the DataFrame
            row_values = row.values
            if all(value == "" for value in row_values):
                errors.append(f"File: {file_name}, Row: {row_number + 1} - All values are empty.")

            for column, value in row.iteritems():
                column = column.strip()
                column_range = value_ranges.get(column)
                if column_range:
                    lower_bound, upper_bound = column_range

                    try:
                        value = float(value)
                        expectation = PandasDataset(df, expectation_suite=suite)  # Use the same PandasDataset object for each row
                        expectation.expect_column_values_to_be_between(column, min_value=lower_bound, max_value=upper_bound)

                        result = expectation.validate()
                        if not result.success:
                            errors.append(f"File: {file_name}, Row: {row_number + 1}, Column: {column} - Value Error: {value}")
                    except ValueError:
                        errors.append(f"File: {file_name}, Row: {row_number + 1}, Column: '{column}' - Invalid numeric value.")

                if pd.isnull(value):
                    errors.append(f"File: {file_name}, Row: {row_number + 1}, Column: '{column}' - Value is empty.")

        error = {'filename': file_name, 'errors': errors}
        if len(errors) > 0:
            # Send Errors to DB
            save_data_logs(session, error)
        else:
            pass


def create_expectation_suite(value_ranges):
    suite = ExpectationSuite('my_suite')

    # Expectations for column value ranges
    for column, value_range in value_ranges.items():
        lower_bound, upper_bound = value_range
        expectation_column_value_range = ExpectationConfiguration(
            expectation_type='expect_column_values_to_be_between',
            kwargs={
                'column': column,
                'min_value': lower_bound,
                'max_value': upper_bound,
                'result_format': 'BASIC'
            },
            meta={
                'notes': f"Values in column '{column}' should be between {lower_bound} and {upper_bound}"
            }
        )
        suite.append_expectation(expectation_column_value_range)
    return suite


def great_expectations_validation(session, csv_folder_path, split_folder):
    split_csv_files(csv_folder_path, split_folder)
    validate_csv_files(session, split_folder)
    pass



database = db_engine()
great_expectations_validation(database['session'], input_file_great_expectations, output_directory_great_expectations)
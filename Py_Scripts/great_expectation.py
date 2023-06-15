import pandas as pd
import numpy as np
import great_expectations as ge
from great_expectations.dataset import PandasDataset
import os
import csv

def read_csv_file(file_path):
    return pd.read_csv(file_path)

def split_csv_into_files(input_file, output_directory, num_files):
    header = pd.read_csv(input_file, nrows=0).columns.tolist()
    total_rows = sum(1 for _ in open(input_file)) - 1
    rows_per_file = total_rows // num_files

    with open(input_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)

        for i in range(1, num_files + 1):
            output_file = f'{output_directory}/output_{i}.csv'
            with open(output_file, 'w', newline='') as outfile:
                csv_writer = csv.writer(outfile)
                csv_writer.writerow(header)
                rows_written = 0
                while rows_written < rows_per_file:
                    try:
                        row = next(csv_reader)
                        csv_writer.writerow(row)
                        rows_written += 1
                    except StopIteration:
                        break

def validate_csv_files(folder_path):
    correct_data = pd.DataFrame()
    columns = ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar', 'chlorides',
               'free sulfur dioxide', 'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol']

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            data = read_csv_file(file_path)
            dataset = PandasDataset(data)

            for column in columns:
                dataset.expect_column_to_exist(column)
                dataset.expect_column_values_to_not_be_null(column)

            value_ranges = {'fixed acidity': (4.6, 15.9), 'volatile acidity': (0.12, 1.58), 'citric acid': (0.0, 1.0),
                            'residual sugar': (0.9, 15.5), 'chlorides': (0.012, 0.611), 'free sulfur dioxide': (1.0, 68.0),
                            'total sulfur dioxide': (6.0, 289.0), 'density': (0.99007, 1.00369), 'pH': (2.74, 4.01),
                            'sulphates': (0.33, 2.0), 'alcohol': (8.4, 14.9)}

            for column, value_range in value_ranges.items():
                dataset.expect_column_values_to_be_between(column, min_value=value_range[0], max_value=value_range[1])

            validation_results = dataset.validate()

            for expectation_result in validation_results["results"]:
                if not expectation_result["success"]:
                    error_type = expectation_result['expectation_config']['expectation_type']
                    error_column = expectation_result['expectation_config']['kwargs']['column']

                    if error_type == "expect_column_values_to_not_be_null":
                        null_rows = data[data[error_column].isnull()]
                        null_rows['Filename'] = [filename] * len(null_rows)
                        null_rows['Error'] = [error_type] * len(null_rows)

                        data = data.drop(null_rows.index)

                    if error_type == "expect_column_values_to_be_between":
                        min_value = expectation_result['expectation_config']['kwargs']['min_value']
                        max_value = expectation_result['expectation_config']['kwargs']['max_value']
                        filtered_rows = data[(data[error_column] < min_value) | (data[error_column] > max_value)]
                        filtered_rows['Filename'] = [filename] * len(filtered_rows)
                        filtered_rows['Error'] = [error_type] * len(filtered_rows)

                        data = data.drop(filtered_rows.index)

            correct_data = pd.concat([correct_data, data], axis=0)

    output_folder_path_correct_data = 'data/Clean_Data'
    output_file_name_correct_data = 'output.csv'
    file_path_correct_data = os.path.join(output_folder_path_correct_data, output_file_name_correct_data)
    correct_data.to_csv(file_path_correct_data, index=False)


def great_expectation(input_file, output_directory):
        split_csv_into_files(input_file, output_directory, 5)
        validate_csv_files(output_directory)
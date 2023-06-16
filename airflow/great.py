import csv
import pandas as pd
import os
import sys
sys.path.append('/Users/kiruba/Documents/GitHub/EPITA_DATA_SCIENCE_IN_PRODUCTION/')
import datetime
from great_expectations.dataset import PandasDataset
from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.core.expectation_configuration import ExpectationConfiguration
from Py_Scripts.save_data_logs import save_data_logs
from Py_Scripts import value_ranges
from Py_Scripts.db_engine import db_engine
from Py_Scripts import input_file_great_expectations, output_directory_great_expectations, invalid_output_file_great_expectations, valid_output_great_expectations


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
                    filename = f"{base_filename}_{filename}"
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


def validate_csv_files(session, file_folder, invalid_output_file_great_expectations, valid_output_great_expectations):
    suite = create_expectation_suite(value_ranges)
    for file_name in os.listdir(file_folder):
        file_path = os.path.join(file_folder, file_name)
        errors = []
        df = pd.read_csv(file_path)

        expectation = PandasDataset(df, expectation_suite=suite)
        results = expectation.validate()
        
        data_quality_issues = results["results"]
        invalid_rows_data = pd.DataFrame(columns=df.columns)
        
        for expectation_result in data_quality_issues:
            if not expectation_result["success"]:
                column = expectation_result["expectation_config"]["kwargs"]["column"]
                partial_unexpected_list = expectation_result["result"]["partial_unexpected_list"]
                invalid_rows_data = invalid_rows_data.append(df[df[column].isin(partial_unexpected_list)])
                errors.append(str(invalid_rows_data))


        df.drop(invalid_rows_data.index, inplace=True)
        base_filename = datetime.datetime.now().strftime("%Y%m%d")

        invalid_output_file_path = os.path.join(invalid_output_file_great_expectations, file_name)
        invalid_rows_data.to_csv(invalid_output_file_path, index=False)

        valid_output_file_path = os.path.join(valid_output_great_expectations, file_name)
        df.to_csv(valid_output_file_path, index=False)
        
        
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



def great_expectations_validation(csv_folder_path, split_folder, invalid_output_file_great_expectations, valid_output_file_great_expectations):
    split_csv_files(csv_folder_path, split_folder)
    engine = db_engine()
    session = engine['session']
    validate_csv_files(session, split_folder, invalid_output_file_great_expectations, valid_output_file_great_expectations)
    pass

# great_expectations_validation(input_file_great_expectations, output_directory_great_expectations, invalid_output_file_great_expectations, valid_output_great_expectations)
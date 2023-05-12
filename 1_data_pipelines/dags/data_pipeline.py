import os
from datetime import datetime, timedelta
import time
import pandas as pd
from typing import List, Dict, Tuple
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from utils import (has_correct_digits,
                   identify_date_format,
                   format_date_of_birth,
                   is_above_age,
                   is_valid_email,
                   is_empty_name,
                   split_name,
                   get_hashed_date
                   )


# define the input and output directories
INPUT_DIR = '/source_data'
OUTPUT_RAW_DIR = '/raw_data'
OUTPUT_FAILED_DIR = '/unsuccessful_applicants'
OUTPUT_PASSED_DIR = '/successful_applicants'


# define the PythonOperator that reads the csv files and processes the records
def ingest_csv_files(path: str) -> List[Dict]:
    # loop through all the csv files in the input directory
    # and store the records into a python dictionary
    # remove the file from source_data folder to prevent duplication
    all_data = []
    for file in os.listdir(path):
        if file.endswith('.csv'):
            filename = os.path.join(path, file)
            df = pd.read_csv(filename)
            print(f'Ingested {filename}')
            data_dict = df.to_dict('records')
            all_data.extend(data_dict)
            os.remove(filename)
            print(f'Removed {filename}')
    return all_data


# define the function to preprocess the data
def preprocess_records(records: List[Dict]) -> List[Dict]:
    # perform initial processing of the records
    preprocessed_records = []
    for record in records:
      preprocessed_record = {}
      preprocessed_record['first_name'], preprocessed_record['last_name'] = split_name(record['name'])
      preprocessed_record['email'] = record['email']
      date_format = identify_date_format(record['date_of_birth'])
      preprocessed_record['date_of_birth'] = format_date_of_birth(record['date_of_birth'], date_format)
      preprocessed_record['mobile_no'] = record['mobile_no']
      preprocessed_record['above_18'] = is_above_age(preprocessed_record['date_of_birth'], 18)
      preprocessed_records.append(preprocessed_record)
    return preprocessed_records


# define the function to perform the validation check
def validate_record(record: dict) -> str:
    # perform validation checks on the record
    # return valid if the record passes the checks and the error otherwise
    if not has_correct_digits(record['mobile_no'], 8):
        return 'invalid_mobile_number'
    if not record['above_18']:
        return 'below_18'
    if not is_valid_email(record['email']):
        return 'invalid_email'
    if (is_empty_name(
        record['first_name']) and is_empty_name(record['last_name']
                                                )):
        return 'missing_name'
    return 'valid'


def validate_records(records: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    # Perform validation checks on all the records
    valid_records = []
    invalid_records = []
    for record in records:
        check = validate_record(record)
        if check == 'valid':
            valid_records.append(record)
        else:
            record['validate_check'] = check
            invalid_records.append(record)
    return valid_records, invalid_records


# define the function to perform the transformation
def transform_records(records: list) -> list:
    # perform transformation on the record
    # return the transformed record
    for record in records:
        record['membership_id'] = '_'.join([record['last_name'],
                                            get_hashed_date(record['date_of_birth'])])
    return records


# define the function to unload the records
def write_dict_to_csv(records: list, path: str, prefix: str):
    # write dict to target path
    # append timestamp to prevent files from overwritten
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{path}/{prefix}_{timestamp}.csv"
    df = pd.DataFrame(records)
    df.to_csv(filename, index=False)
    print(f"{len(records)} records written to {filename}")


# set up the pipeline
default_args = {
  'owner': 'airflow',
  'depends_on_past': False,
  'start_date': datetime(2022, 1, 1),
  'retries': 1,
  'retry_delay': timedelta(minutes=5),
}

dag = DAG(
  dag_id='data_pipeline',
  default_args=default_args,
  schedule_interval="@hourly",
  catchup=False,
  description='Data pipeline to process ecommerce data',
)


def ingestion(**context):
    raw_data = ingest_csv_files(INPUT_DIR)
    if len(raw_data) > 0:
      write_dict_to_csv(raw_data, OUTPUT_RAW_DIR, 'raw_data')
    context['ti'].xcom_push(key='raw_data', value=raw_data)


def preprocessing(**context):
    raw_data = context['ti'].xcom_pull(key='raw_data')
    preprocessed_data = preprocess_records(raw_data)
    context['ti'].xcom_push(key='preprocessed_data', value=preprocessed_data)


def validation(**context):
    preprocessed_data = context['ti'].xcom_pull(key='preprocessed_data')
    valid_data, invalid_data = validate_records(preprocessed_data)
    if len(invalid_data) > 0:
      write_dict_to_csv(invalid_data, OUTPUT_FAILED_DIR, 'unsuccessful_applicants')
    context['ti'].xcom_push(key='valid_data', value=valid_data)


def transformation(**context):
    valid_data = context['ti'].xcom_pull(key='valid_data')
    if len(valid_data) > 0:
      transformed_data = transform_records(valid_data)
      write_dict_to_csv(transformed_data, OUTPUT_PASSED_DIR, 'successful_applicants')


with dag:
    ingestion = PythonOperator(
      task_id='ingestion',
      python_callable=ingestion,
      provide_context=True,
    )

    preprocessing = PythonOperator(
      task_id='preprocessing',
      python_callable=preprocessing,
      provide_context=True,
    )

    validation = PythonOperator(
      task_id='validation',
      python_callable=validation,
      provide_context=True,
    )

    transformation = PythonOperator(
      task_id='transformation',
      python_callable=transformation,
      provide_context=True,
    )

    ingestion >> preprocessing >> validation >> transformation

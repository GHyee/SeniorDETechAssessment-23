import os
import boto3
import csv
import io
import time
from typing import List, Dict, Tuple
from utils import (has_correct_digits,
                   identify_date_format,
                   format_date_of_birth,
                   is_above_age,
                   is_valid_email,
                   is_empty_name,
                   split_name,
                   get_hashed_date
                   )

# Define the S3 bucket and partitions
BUCKET_NAME = os.environ['BUCKET_NAME']
# define the input and output partitions
INPUT_PREFIX = 'source_data'
OUTPUT_RAW_PREFIX = 'raw_data'
OUTPUT_FAILED_PREFIX = 'unsuccessful_applicants'
OUTPUT_PASSED_PREFIX = 'successful_applicants'


def ingest_csv_files(prefix: str) -> List[Dict]:
    # Loop through all the CSV files in the S3 bucket
    # and store the records into a Python dictionary
    # Remove the file from source_data folder to prevent duplication
    all_data = []
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(os.environ['BUCKET_NAME'])
    for obj in bucket.objects.filter(Prefix=prefix):
        if obj.key.endswith('.csv'):
            obj_content = obj.get()['Body'].read().decode('utf-8').splitlines()
            reader = csv.DictReader(obj_content)
            for row in reader:
                all_data.append(row)
            s3.Object(bucket.name, obj.key).delete()
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
def write_dict_to_s3_csv(records: list, bucket_name: str, prefix: str):
    # write dict to target S3 bucket
    # append timestamp to prevent files from overwritten
    if len(records) > 0:
      timestamp = time.strftime("%Y%m%d-%H%M%S")
      filename = f"{prefix}/{prefix}_{timestamp}.csv"
      s3 = boto3.client("s3")
      csv_buffer = io.StringIO()
      writer = csv.DictWriter(csv_buffer, fieldnames=records[0].keys())
      writer.writeheader()
      writer.writerows(records)
      s3.put_object(Bucket=bucket_name, Key=filename, Body=csv_buffer.getvalue())
      print(f"{len(records)} records written to s3://{bucket_name}/{prefix}/{filename}")


def lambda_handler(event, context):
    # Read CSV files from S3
    raw_data = ingest_csv_files(INPUT_PREFIX)
    if len(raw_data) > 0:
        write_dict_to_s3_csv(raw_data, BUCKET_NAME, OUTPUT_RAW_PREFIX)

    # Perform data processing
    preprocessed_data = preprocess_records(raw_data)
    valid_data, invalid_data = validate_records(preprocessed_data)
    transformed_data = transform_records(valid_data)

    # Write output files to S3
    write_dict_to_s3_csv(invalid_data, BUCKET_NAME, OUTPUT_FAILED_PREFIX)
    write_dict_to_s3_csv(transformed_data, BUCKET_NAME, OUTPUT_PASSED_PREFIX)

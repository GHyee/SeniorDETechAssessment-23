# Data Pipelines

## Problem statement:
Design and implement a pipeline to process the membership applications submitted by users on an hourly interval.

## Data Pipeline Design
The data pipeline is built using Airflow with python and it consists of several python operators to ingest, preprocess, validate and transform the data.
Some additional features includes:
- Storing raw data in a separate folder for backup purpose.
- Adding the reason to the failed records before storing them in a separate folder for analysis and troubleshooting.

![alt text](https://github.com/ghyee/SeniorDETechAssessment-23/blob/main/images/data-pipeline.jpg?raw=true)

## Installation
Airflow and Docker are required to execute this data pipeline. To install Airflow, run the following code:
```bash
pip install "apache-airflow[celery]==2.6.0" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.6.0/constraints-3.7.txt"
```
Follow the [guide](https://docs.docker.com/engine/install/) on Docker's website to install Docker engine and [docker-compose](https://docs.docker.com/compose/install/).

## Usage
To run the pipeline, execute the following codes:
```bash
cd 1_data_pipelines
docker-compose up --build
```
The Airflow instance should be deployed and running on the [localhost](http://0.0.0.0:8080/admin/).


Note that the following paths on the local machine are mounted to the Docker container to read and write the records. The processed files will be stored in the local machine once it is ready. If the paths are not already created, it should be created when the above code is executed.
```yaml
volumes:
  - ./dags:/usr/local/airflow/dags
  - ./source_data:/source_data
  - ./raw_data:/raw_data
  - ./cleaned_data:/cleaned_data
  - ./failed_data:/failed_data
```

To activate the pipeline, go to the console and click on the `On` button.
Note that the CSV files should be stored in the [source_data](/1_data_pipelines/source_data) folder. If the files are dropped after the pipeline is activated, the processing will only kick off in the next hour.

## Data flow
### 1. Ingestion
At the ingestion stage, all the CSV files are ingested and the source file will be removed to prevent duplication. The ingested data will be written to the [raw_data](/1_data_pipelines/raw_data) folder for backup purpose.

### 2. Preprocessing
Once the data are ingested, the following steps are executed to preprocess the data.
1. Splitting of the `name` field to `first_name` and `last_name`.
2. Changing of the date format for `date_of_birth` field to YYYYMMDD format.
3. Addition of new field `above_18` to check if applicant is above 18 years old as of 1st Jan 2022.

### 3. Validation
The following validations will be performe on the preprocessed data:
1. Check if the field `mobile_no` has 8 digit.
2. Check if applicant is above 18 years old as of 1st Jan 2022.
3. Check if the field `email` ends with `@emailprovider.com` or `@emailprovider.net`.
4. Check if either `first_name` and `last_name` are not empty.

The records that successfully pass all the validation will be further processed while the failed records are stored as CSV files in the [failed_data](/1_data_pipelines/failed_data) folder. The reason of validation failure will also be found in the `validation_check` field.

**Sample failed data**:

| first_name | last_name | email                              | date_of_birth | mobile_no | above_18 | validate_check      |
|------------|-----------|------------------------------------|---------------|-----------|----------|---------------------|
| William    | Dixon     | William_Dixon@woodward-fuller.biz  | 19860110      | 40601711  | True     | invalid_email       |
| Kristen    | Horn      | Kristen_Horn@lin.com               | 19740910      | 737931    | True     | invalid_mobile_number |
| Kimberly   | Chang     | Kimberly_Chang@johnson-lopez.biz   | 19740227      | 2692047   | True     | invalid_mobile_number |
| Mary       | Ball      | Mary_Ball@stevens.biz              | 19680502      | 886359    | True     | invalid_mobile_number |


### 4. Transformation
The valid data will further processed at the transformation stage. The below fields will be added to the records.
1. `membership_id` - Concatenation of the `last_name` field, followed by a SHA256 hash of the applicant's `date_of_birth`, truncated to first 5 digits of hash (i.e <last_name>_<hash(YYYYMMDD)>).

The transformed data will then be stored in the [cleaned_data](/1_data_pipelines/cleaned_data) folder.
Note: the hashing is performed on the YYYYMMDD string of the `date_of_birth` field.


**Sample cleaned data**:

first_name | last_name | email                              | date_of_birth | mobile_no | above_18 | membership_id
---------- | --------- | ---------------------------------- | ------------- | --------- | -------- | -------------
Patty      | Smith     | Patty_Smith@ross.com              | 19750827      | 59428759  | True     | Smith_c7677
Sean       | Wang      | Sean_Wang@gibson-calderon.com     | 19600311      | 25595367  | True     | Wang_04168
Richard    | Estrada   | Richard_Estrada@malone.com        | 19921015      | 22821527  | True     | Estrada_0bf5b
Jackson    | Cline     | Jackson_Cline@hudson.net           | 19710121      | 48056519  | True     | Cline_825fb
Allen      | Williams  | Allen_Williams@sanchez.net         | 19971109      | 77991519  | True     | Williams_3e726


### 5. Output
The processed files are saved to the following paths:
1. successful application - [cleaned_data](/1_data_pipelines/cleaned_data/)
2. unsuccessful application - [failed_data](/1_data_pipelines/failed_data/)
3. backup of source data - [source_data](/1_data_pipelines/source_data/)

## Limitations
1. Date format for `date_of_birth` field does not follow a fixed format. This leads to an issue when the month and date values are interchangeable. For example, `08/09/1965` can be intepreted as 8th September 1965 or 9th August 1965 	:singapore:. This will also result in confusion when the processing the age and leading to valid records being marked as unsuccessful applications. The current implementation assumes the commonly adopted date format for Singapore, which follows `dd-mm-yyyy` format to resolve the conflict.

2. The data processing functions are not fully optimised due to time constraint. Possible performance boost could be achieved by vectorizing some of the operations in Pandas DataFrame.

3. The data transformation step is hardcoded but it can be decoupled into a configuration file. This will be useful for future development when more transformation steps are required.
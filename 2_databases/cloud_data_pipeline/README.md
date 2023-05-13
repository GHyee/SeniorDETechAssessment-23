# Cloud data pipeline

## Problem statement:
Design and implement a pipeline on cloud that processes membership applications and determine if an application is successful or unsuccessful. Applications are dropped into a location for processing.

## Cloud data pipeline Design

### Deploy Airflow to cloud
The data pipeline designed in [section 1](../1_data_pipelines/) is already dockerised so it can be deployed on cloud on a EC2 instance.
The data pipeline is currently reading and writing data from the mounted volume. When migrating to cloud, one enhancement we can do is to modify the codes to read and write from s3 instead. This is might the data ingestion and retrieval process easier to integrate with other services.

### Fully cloud native pipeline
Another alternative is to fully use AWS native services to design the pipeline. This is reduce the maintenance effort and might be more cost effective and scalable.

**Architecture Design**

1. AWS S3 bucket for storing the membership applications and processed files.
- A partition can be created to receive the applications. When a new file is dropped in this partition, the pipeline will be triggered.
- Partitions can also be created to store the successfully and unsuccessfully processed files.
- The backup of the source file can also be stored in a separate partition.

2. AWS Lambda to write the code for processing the membership applications.
- The Lambda function can execute the application processing code, which has already been written.
- The application processing code will determine if the application is successful or not and generate a membership ID if the application is successful.
- If the application is successful, the Lambda function should upload the membership application and the membership ID to a separate partition in the AWS S3 bucket for successful applications.
- If the application is unsuccessful, the Lambda function should move the application to a separate partition in the AWS S3 bucket for unsuccessful applications.

![sample lambda logs](/images/lambda_logs.png)

3. AWS CloudWatch can be used to execute the lambda on an hourly basis. It also stores the log of the Lambda function activity and set up an alarm in case of errors.

![eventbridge rule](/images/event_bridge.png)

**Implementation**
The above pipeline can be implemented and managed through Terraform, a  Infrastructure as Code (IaC) tool. The terraform scripts are saved in the [terraform](/2_databases/cloud_data_pipeline/terraform/) folder.
The python scripts to be executed by the Lambda function is saved in [terraform/src](/2_databases/cloud_data_pipeline/terraform/src/) folder.

Assuming that Terraform in already installed, follow the below steps to deploy the resources.

1. Initialize a working directory containing Terraform configuration files.
```
cd terraform
terraform init
```

2. Create an execution plan and preview the changes that Terraform plans to make to the cloud infrastructure.
```
terraform plan
```

3. Deploy the resources.
```
terraform apply -auto-approve
```

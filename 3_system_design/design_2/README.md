# Design 2 - Cloud Data Infrastructure

## Problem statement
Design a cloud data infrastructure that can ingest image data. The considerations includes:
1. Ingestion
The data can be sent through API or Kafka stream.
2. Processing
The data has to be processed on cloud by using executing a provided script.
3. Storage and Retention
The images and its metadata has to be stored in the cloud environment for 7 days, after which it has to be purged from the environment for compliance and privacy.
4. Consumption
A Business Intelligence resource where the company's analysts can access and perform analytical computation on the data stored has to be provisioned.
5. Access Control
Acceess contol has to be managed in a scalable manner
6. Security
Security of data at rest and in transit
7. Cost
Scaling to meet user demand while keeping costs low
8. Maintainance
Maintainance of the environment and assets (including processing scripts)
9. Cloud computing best practices
Architecture should takes into account best practices such as:
- Managability
- Scalability
- Secure
- High Availability
- Elastic
- Fault Tolerant and Disaster Recovery
- Efficient
- Low Latency
- Least Privilege

## Generating the diagram
To generate the below architecture diagram, follow the below steps:
1. Install required python package.
```
pip install -r requirements.txt
```
2. Execute python script.
```
cd src
python -m generate_diagram 
```

## Description of the Architecture

![data_lake_architecture.png](/3_system_design/design_2/src/data_lake_architecture.png)

The architecture above is designed to meet the requirements of the company's image processing pipeline. The image processing pipeline is initiated when a user uploads an image through the web application or when an image is uploaded to the Kafka stream. The pipeline then processes the image using AWS Lambda, and stores the image and its metadata in a data lake. The data in the data lake can then be accessed and analyzed by the company's analysts using Amazon QuickSight.

### Data Lake
The data lake is composed of the following components:

Amazon S3: Amazon S3 is used to store the images and their metadata. The S3 bucket is configured to automatically purge data after 7 days, as per the requirements of the stakeholders.

AWS Glue: AWS Glue is used to automatically discover and catalog the metadata of the images stored in S3. It provides the ability to query the data using standard SQL queries, and also allows for the creation of ETL pipelines.

AWS Lake Formation: AWS Lake Formation is used to enable fine-grained access control to the data stored in the data lake. It provides the ability to set up policies that restrict access to the data to specific users or groups, and also provides auditing and logging capabilities.

### Image Processing
The image processing component is composed of the following components:

AWS Lambda: AWS Lambda is used to process the images uploaded by users through the web application or through the Kafka stream. The Lambda function is triggered by an S3 event when an image is uploaded to the S3 bucket. The Lambda function processes the image and stores the image and its metadata in the S3 bucket.

### Data Analysis
The data analysis component is composed of the following components:

Amazon QuickSight: Amazon QuickSight is used to analyze and visualize the data stored in the data lake. QuickSight provides the ability to create dashboards and reports that can be shared with other users.
Amazon Redshift: Amazon Redshift Spectrum is used to query the curated data in S3. To optimize the cost, AWS Redshift Serverless, which scales up automtically, can be considered.

## Key Points Addressed
**Securing Access to the Environment and its Resources as the Company Expands**

AWS Lake Formation is used to enable fine-grained access control to the data stored in the data lake. This provides the ability to set up policies that restrict access to the data to specific users or groups, and also provides auditing and logging capabilities.

**Security of Data at Rest and in Transit**

Data at rest is secured by storing it in an S3 bucket configured to automatically purge data after 7 days. Data in transit is secured by using SSL/TLS encryption to encrypt data transmitted between components.

**Scaling to Meet User Demand While Keeping Costs Low**

AWS Lambda can scale automatically to meet user demand. S3 is designed to scale to accommodate any amount of data stored, and AWS Glue, Redshift Serverless and QuickSight can also scale as needed.

**Maintenance of the Environment and Assets** (Including Processing Scripts)
AWS Lambda, Glue, QuickSight and S3 are fully managed services, which means that the infrastructure and assets are automatically maintained by AWS. Automatic deployment and updates can also be managed through IaC using AWS Cloud Formation or Terraform.
Use CloudWatch for monitoring and logging

**Best Practices**
Design for High Availability with multi-AZ deployment
Design for Fault Tolerance and Disaster Recovery with cross-region replication and backups
Use Fine Grain Access Control with Lake Formation and Quicksight for data access control
Use Least Privilege with IAM roles and policies for secure access control

## Assumptions
1. The web application and Kafka stream have features built in to ensure only valid image data are sent over to the data infrastructure.
2. The image processing can be executed in AWS Lambda and it does not exceed the AWS Lambda resource limit in terms of time and memory. Alternatively, we can use other AWS services such as Amazon ECS or Amazon EKS to run the image processing jobs in containers, which can provide more flexibility and scalability for larger image processing workloads. 
3. It is important to monitor the Lambda function and image processing jobs to ensure that they are within the allotted time and memory limits, and to take appropriate actions if they exceed those limits.
4. The expected number of image to be processed concurrently will not exceed the limit of 1000. Otherwise, a request has to be made to increase the limit or AWS Batch will be used to process the data in batches instead of triggering it upon arrival of a new file.
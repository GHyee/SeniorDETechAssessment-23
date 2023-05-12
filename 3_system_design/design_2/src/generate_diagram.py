from diagrams import Cluster, Diagram
from diagrams.aws.analytics import Glue, Quicksight, ManagedStreamingForKafka
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Redshift
from diagrams.aws.storage import S3

with Diagram("Data Lake Architecture", show=False):

    with Cluster("API"):

        with Cluster("Web Application"):
            api = Lambda("Lambda Function")
            s3_api = S3("S3")

        api >> s3_api

    with Cluster("Kafka Stream"):
        kafka = ManagedStreamingForKafka("Kafka Cluster")
        s3_kafka = S3("S3")

        kafka >> s3_kafka

    with Cluster("ETL"):
        glue = Glue("AWS Glue")
        s3_raw = S3("S3 Raw Data")
        s3_curated = S3("S3 Curated Data")

        s3_api >> s3_raw
        s3_kafka >> s3_raw

        glue << s3_raw
        glue >> s3_curated

    with Cluster("Analytics"):
        quicksight = Quicksight("Quicksight")
        redshift = Redshift("Redshift")

        quicksight >> redshift >> s3_curated

    with Cluster("Archival"):
        s3_archive = S3("S3 Archive")

        s3_curated >> s3_archive

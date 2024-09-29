# Liquor Store ETL with Google Cloud Dataproc and PySpark

## Overview
This project automates an ETL (Extract, Transform, Load) workflow using Google Cloud Dataproc and PySpark to process data from the public Iowa Liquor Sales dataset stored in BigQuery. The project uses Terraform to provision the necessary Google Cloud infrastructure, including a Dataproc cluster and a Google Cloud Storage (GCS) bucket. The goal is to extract the liquor sales data, apply transformations using PySpark, and load the processed data back into BigQuery for further analysis.

## Purpose
The primary purpose of this project is to demonstrate the end-to-end automation of an ETL pipeline with pyspark in Google Cloud Platform (GCP) using infrastructure-as-code principles with Terraform. 

## Key Technologies
Google Cloud Platform: Dataproc, BigQuery, Cloud Storage
Terraform: Infrastructure as Code (IaC) to automate resource provisioning
PySpark: Distributed data processing using Apache Spark
GitHub Actions: CI/CD to automate deployments and job execution

## Data source (Iowa liquor sales dataset):
Is publicly available at: 
https://console.cloud.google.com/bigquery?_ga=2.8611638.288326788.1726990215-459272757.1699721835&project=mybookdashboard&ws=!1m5!1m4!4m3!1sbigquery-public-data!2siowa_liquor_sales!3ssales

The Iowa Liquor Sales dataset was chosen because it is publicly available and can demonstrate the types of business questions one could explore in a real business scenario. The ETL process in this project is designed to help business analysts answer key questions that could improve sales and revenue. For example, the transformed data allows analysts to identify top-performing retailers, discover the most popular product categories, and assess which vendors contribute the least to overall sales—insights that are critical for driving data-driven decisions in a retail environment.

## Improvements
- add a linter to yml
- adjust tf to add biq query table to load data to
- adjust main.py to load data into giq query table
- big query script to analyst the transformed dataset to answer possible business questions 

## Development
#### Code to run locally and some set up: 
- create gcp project
- create service account with roles:
    - BigQuery Admin
    - BigQuery Data Editor
    - Dataproc Administrator
    - Storage Admin
    - Storage Object Admin
- create bucket for terraform state file: 
gsutil mb -l us-central1 gs://liquor-store-terraform-state
- update subnet (?) private gcp access 
- git push and yml runs terraform if file is changed, and run workflow template with pyspark job

#### Run locally:
```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```
```
$ brew tap hashicorp/tap
$ brew install hashicorp/tap/terraform
$ terraform init
$ terraform plan
$ terraform apply
```

#### Set up dataproc cluster using google shell: 
```
gcloud dataproc workflow-templates set-managed-cluster liquor-etl-workflow \
  --region us-central1 \
  --cluster-name liquor-etl-workflow-jobs \
  --zone us-central1-a \
  --master-machine-type n1-standard-2 \
  --master-boot-disk-type pd-balanced \
  --master-boot-disk-size 50GB \
  --num-workers 2 \
  --worker-machine-type n1-standard-2 \
  --worker-boot-disk-type pd-balanced \
  --worker-boot-disk-size 50GB \
```

```
cloud dataproc workflow-templates add-job pyspark \
  gs://liquor-store-data-bucket/script/main.py \
  --step-id job-a722fda0 \
  --workflow-template liquor-etl-workflow \
  --region us-central1
```

```
gcloud compute networks subnets update default \
  --region us-central1 \
  --enable-private-ip-google-access
```

```
gcloud dataproc workflow-templates instantiate liquor-etl-workflow \
  --region us-central1
```

```

 gcloud dataproc workflow-templates delete liquor-store-etl-workflow   --region=us-central1
```

# liqour-sales-spark-etl

Develop to do: 
- clean up repo
- describe in readme file

- add a linter to yml
- add biq query to tf, github actions and script 
- big query analyse results examples


take data from: 
https://console.cloud.google.com/bigquery?_ga=2.8611638.288326788.1726990215-459272757.1699721835&project=mybookdashboard&ws=!1m5!1m4!4m3!1sbigquery-public-data!2siowa_liquor_sales!3ssales

do some transformations
store data in big query again

answer questions: 
help business analyst figure a=out how to improve sales and revenue
- top retailers by sale
- top categories
- min vendors selling sale
- min vendrors cetegories selling litres / sale compared to others. 






# running spark locally
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt





# 
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
  --max-idle 10m


cloud dataproc workflow-templates add-job pyspark \
  gs://liquor-store-data-bucket/script/main.py \
  --step-id job-a722fda0 \
  --workflow-template liquor-etl-workflow \
  --region us-central1


gcloud compute networks subnets update default \
  --region us-central1 \
  --enable-private-ip-google-access


gcloud dataproc workflow-templates instantiate liquor-etl-workflow \
  --region us-central1


 gcloud dataproc workflow-templates delete liquor-store-etl-workflow   --region=us-central1
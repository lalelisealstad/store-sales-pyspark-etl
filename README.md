# liqour-sales-spark-etl

Develop to do: 

- develop extract and transform locally
- add big query table create to tf a
- develop load locally
- add dataproc to terraform 
- run job on data proc
- use github actions to deploy when new changed in main
- big query analyse results examples

- clean up repo
- describe in readme file


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

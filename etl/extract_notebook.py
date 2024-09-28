# %%
# set working directory to same place as main.py to import programs the same way as the app
import os
current_directory = os.getcwd()
if '/etl' in current_directory:
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    os.chdir(parent_directory)
os.getcwd()

# %%
from pyspark.sql import SparkSession
from pyspark.sql.types import * 
from pyspark.sql.functions import round, col, abs, concat, lit
from pyspark.sql import functions as F


# %%


# Set GCP project ID and dataset details
project_id = 'bigquery-public-data'
dataset = 'iowa_liquor_sales'
table = 'sales'



spark = SparkSession.builder \
    .appName('BigQuery Iowa Liquor Sales') \
    .getOrCreate()

# # Read the BigQuery data into a DataFrame
# df = spark.read \
#     .format('bigquery') \
#     .option('project', project_id) \
#     .option('dataset', dataset) \
#     .option('table', table) \
#     .load()

# Show a few rows from the dataset
# Optionally stop the Spark session
# spark.stop()


# %%
file_path = 'test_data/bquxjob_3567bd65_1921a4602ae.csv'

# Read the CSV file using PySpark
df = spark.read.option("header", "true").csv(file_path)

# Show the first 10 rows
df.show(10)

# %%
df_filtered = df.select(['store_name',
                        'category_name',
                        'item_description',
                        'bottle_volume_ml',
                        'vendor_number',                        
                        'state_bottle_cost',
                        'state_bottle_retail',
                        'sale_dollars',
                        'bottles_sold'])

# %%
# change dtypes 

dtypes= {
        'bottle_volume_ml' : 'double',
        'vendor_number' : 'int',
        'state_bottle_retail' : 'double',
        'state_bottle_cost' : 'double',
        'sale_dollars' : 'double',
        'bottles_sold' : 'int',
        'bottle_volume_ml' : 'int'
}

# Loop through the dictionary to cast each column
for col_name, new_dtype in dtypes.items():
    df_filtered = df_filtered.withColumn(col_name, col(col_name).cast(new_dtype))
    
df_filtered.printSchema()

# %%
# create columns
df_filtered = df_filtered.withColumn('sale_dollars', abs(col('sale_dollars'))) \
                         .withColumn('bottles_sold', abs(col('bottles_sold')))

df_filtered = df_filtered.withColumn('cost_dollars',round(col('state_bottle_cost') * col('bottles_sold'), 2))
df_filtered = df_filtered.withColumn('revenue_dollars', round(col('sale_dollars') - col('cost_dollars'), 2))

df_filtered = df_filtered.withColumn('item_description', concat(col('item_description'), lit(' '), col('bottle_volume_ml'), lit('ml')))

# %%
df_filtered.show()

# %%
df_grouped = df_filtered.groupBy(
    'store_name', 'item_description', 'vendor_number', 'state_bottle_cost', 'state_bottle_retail', 'category_name'
).agg(
    F.round(F.sum('sale_dollars'), 2).alias('total_sale_dollars'),
    F.sum('bottles_sold').alias('total_bottles_sold'),  # No need to round bottles_sold if it's an integer
    F.round(F.sum('cost_dollars'), 2).alias('total_cost_dollars'),
    F.round(F.sum('revenue_dollars'), 2).alias('total_revenue_dollars')
).orderBy(F.col('total_revenue_dollars').desc())

df_grouped.show()


# %%




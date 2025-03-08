from pyspark.sql import SparkSession
from pyspark.sql.types import * 
from pyspark.sql.functions import round, col, abs, concat, lit
from pyspark.sql import functions as F
from google.cloud import bigquery

# Set GCP project ID and dataset details
public_project_id = 'bigquery-public-data'
public_dataset = 'iowa_liquor_sales'
public_table = 'sales'

dataset_id = "store-etl-121.store_dw_output"
table_id = f"{dataset_id}.liquor_sales_transformed"

# BQ schema
schema = [
    bigquery.SchemaField("store_name", "STRING"),
    bigquery.SchemaField("item_description", "STRING"),
    bigquery.SchemaField("vendor_number", "INTEGER"),
    bigquery.SchemaField("state_bottle_cost", "FLOAT"),
    bigquery.SchemaField("state_bottle_retail", "FLOAT"),
    bigquery.SchemaField("category_name", "STRING"),
    bigquery.SchemaField("total_sale_dollars", "FLOAT"),
    bigquery.SchemaField("total_bottles_sold", "INTEGER"),
    bigquery.SchemaField("total_cost_dollars", "FLOAT"),
    bigquery.SchemaField("total_revenue_dollars", "FLOAT"),
]


def create_bq_table_if_not_exists():
    """Creates the BigQuery table if it does not exist."""
    client = bigquery.Client()
    table = bigquery.Table(table_id, schema=schema)
    client.create_table(table, exists_ok=True)
    print(f"BigQuery table {table_id} is ready.")


def transform(df): 
    print('Start transforming DataFrame...')
    
    df_filtered = df.select([
        'store_name', 'category_name', 'item_description',
        'bottle_volume_ml', 'vendor_number', 'state_bottle_cost',
        'state_bottle_retail', 'sale_dollars', 'bottles_sold'
    ])
    
    # Define column data types
    dtypes = {
        'bottle_volume_ml': 'int',
        'vendor_number': 'int',
        'state_bottle_retail': 'double',
        'state_bottle_cost': 'double',
        'sale_dollars': 'double',
        'bottles_sold': 'int'
    }

    # Change column data types
    for col_name, new_dtype in dtypes.items():
        df_filtered = df_filtered.withColumn(col_name, col(col_name).cast(new_dtype))

    # Create new columns
    df_filtered = df_filtered.withColumn('sale_dollars', abs(col('sale_dollars'))) \
                             .withColumn('bottles_sold', abs(col('bottles_sold'))) \
                             .withColumn('cost_dollars', round(col('state_bottle_cost') * col('bottles_sold'), 2)) \
                             .withColumn('revenue_dollars', round(col('sale_dollars') - col('cost_dollars'), 2)) \
                             .withColumn('item_description', concat(col('item_description'), lit(' '), col('bottle_volume_ml'), lit('ml')))

    df_grouped = df_filtered.groupBy(
        'store_name', 'item_description', 'vendor_number',
        'state_bottle_cost', 'state_bottle_retail', 'category_name'
    ).agg(
        F.round(F.sum('sale_dollars'), 2).alias('total_sale_dollars'),
        F.sum('bottles_sold').alias('total_bottles_sold'),  
        F.round(F.sum('cost_dollars'), 2).alias('total_cost_dollars'),
        F.round(F.sum('revenue_dollars'), 2).alias('total_revenue_dollars')
    ).orderBy(F.col('total_revenue_dollars').desc())

    print('DataFrame transformation complete.')
    return df_grouped


def main():
    # Path to the BigQuery connector JAR
    bigquery_connector_path = "gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.41.0.jar"

    # Start a PySpark session with BigQuery connector
    spark = SparkSession.builder \
        .appName('BigQuery Iowa Liquor Sales') \
        .config('spark.jars', bigquery_connector_path) \
        .config('spark.sql.execution.arrow.pyspark.enabled', 'true') \
        .config("spark.hadoop.fs.gs.system.bucket", "store-etl-121-temp-bucket") \
        .getOrCreate()

    print("Extracting data from BigQuery...")
    df = spark.read \
        .format('bigquery') \
        .option('project', public_project_id) \
        .option('dataset', public_dataset) \
        .option('table', public_table) \
        .load()

    print('DataFrame extracted from BigQuery')

    try:
        df_transformed = transform(df)
        df_transformed.show()

        create_bq_table_if_not_exists()

        df_limited = df_transformed.limit(10)

        print("Writing first 10 rows to BigQuery...")

        # Write the transformed and limited DataFrame to BigQuery
        df_limited.write \
            .format("bigquery") \
            .option("table", table_id) \
            .mode("append") \
            .save()

        print("Successfully written first 10 rows to BigQuery.")

    except Exception as e:
        print("Transformation or Load failed:", e)
        raise

    spark.stop()


if __name__ == "__main__":
    main()

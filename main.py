from pyspark.sql import SparkSession
from etl.transform import transform 


def main():
    # Path to the BigQuery connector JAR
    bigquery_connector_path = 'gs://spark-lib/bigquery/spark-bigquery-latest.jar'

    # Start a PySpark session with BigQuery connector
    spark = SparkSession.builder \
        .appName('BigQuery Iowa Liquor Sales') \
        .config('spark.jars', bigquery_connector_path) \
        .config('spark.sql.execution.arrow.pyspark.enabled', 'true') \
        .getOrCreate()

    # Set GCP project ID and dataset details
    public_project_id = 'bigquery-public-data'
    public_dataset = 'iowa_liquor_sales'
    public_table = 'sales'

    # Read the BigQuery data into a DataFrame
    df = spark.read \
        .format('bigquery') \
        .option('project', public_project_id) \
        .option('dataset', public_dataset) \
        .option('table', public_table) \
        .load()

    print('Dataframe extracted from big query')
    
    df_transformed = transform(df)
    
    print('Dataframe transformed')
    
    # load to big query
    df_transformed.show()
    
    
    spark.stop()

if __name__ == "__main__":
    main()
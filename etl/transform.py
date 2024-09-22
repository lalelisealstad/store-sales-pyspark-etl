from pyspark.sql import SparkSession
from pyspark.sql.types import * 
from pyspark.sql.functions import round, col, abs, concat, lit
from pyspark.sql import functions as F


def transform(df): 
    print('start transforming df')
    df_filtered = df.select(['store_name',
                        'category_name',
                        'item_description',
                        'bottle_volume_ml',
                        'vendor_number',                        
                        'state_bottle_cost',
                        'state_bottle_retail',
                        'sale_dollars',
                        'bottles_sold'])
    
    
    dtypes= {
        'bottle_volume_ml' : 'double',
        'vendor_number' : 'int',
        'state_bottle_retail' : 'double',
        'state_bottle_cost' : 'double',
        'sale_dollars' : 'double',
        'bottles_sold' : 'int',
        'bottle_volume_ml' : 'int'
    }

    # change dtypes
    for col_name, new_dtype in dtypes.items():
        df_filtered = df_filtered.withColumn(col_name, col(col_name).cast(new_dtype))
        
    
    # create columns
    df_filtered = df_filtered.withColumn('sale_dollars', abs(col('sale_dollars'))) \
                            .withColumn('bottles_sold', abs(col('bottles_sold')))

    df_filtered = df_filtered.withColumn('cost_dollars',round(col('state_bottle_cost') * col('bottles_sold'), 2))
    df_filtered = df_filtered.withColumn('revenue_dollars', round(col('sale_dollars') - col('cost_dollars'), 2))

    df_filtered = df_filtered.withColumn('item_description', concat(col('item_description'), lit(' '), col('bottle_volume_ml'), lit('ml')))
    
    df_grouped = df_filtered.groupBy(
        'store_name', 'item_description', 'vendor_number', 'state_bottle_cost', 'state_bottle_retail', 'category_name'
    ).agg(
        F.round(F.sum('sale_dollars'), 2).alias('total_sale_dollars'),
        F.sum('bottles_sold').alias('total_bottles_sold'),  
        F.round(F.sum('cost_dollars'), 2).alias('total_cost_dollars'),
        F.round(F.sum('revenue_dollars'), 2).alias('total_revenue_dollars')
    ).orderBy(F.col('total_revenue_dollars').desc())

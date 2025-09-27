from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp
# need to do this in .py file but auto avaiable in notebook file
# Create or get existing Spark session
spark = SparkSession.builder.getOrCreate()

def load_and_register_csv_as_table(csv_path, catalog, schema, table):
    """
    Loads a CSV file and saves it as a managed table in Unity Catalog.

    Parameters:
        csv_path (str): The path to the CSV file (e.g., dbfs:/...).
        catalog (str): The Unity Catalog name (e.g., workspace).
        schema (str): The schema/database name (e.g., default).
        table (str): The table name to create or replace.

    Returns:
        DataFrame: The DataFrame loaded from the CSV.
    """
    
    full_table_name = f"{catalog}.{schema}.{table}"
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(csv_path)
    )
    spark.sql(f"DROP TABLE IF EXISTS {full_table_name}")
    df.write.saveAsTable(full_table_name)
    return df

def add_ingestion_date(df,column_name="default_ingestion_date_arg"	):
    """
    Adds an ingestion date column to the DataFrame.

    Parameters:
        df (DataFrame): The DataFrame to add the column to.

    Returns:
        DataFrame: The DataFrame with the added column.
    """
    return df.withColumn(column_name, current_timestamp())
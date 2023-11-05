from pyflink.table import *
from pyflink.table.catalog import HiveCatalog

# creating table environment
env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)

# specify connector to kafka
# t_env.get_config().get_configuration().set_string(
#     "pipeline.jars", 
#     "file:///flink/flink-sql-connector-kafka_2.11-1.11.6.jar"
# )

catalog_name = "myhive"
default_database = "mydatabase"
hive_conf_dir = "/opt/hive_conf"

hive_catalog = HiveCatalog(catalog_name, default_database, hive_conf_dir)
t_env.register_catalog("myhive", hive_catalog)

# Specify hive catalogue
t_env.use_catalog("myhive")

# # Define source table DDL
# source_ddl="""
#     CREATE TABLE nifty_processed(
#     open_val DOUBLE,
#     high_val DOUBLE, 
#     low_val DOUBLE,
#     close_val DOUBLE,
#     volume_val DOUBLE
#     ) WITH (
#     'connector' = 'kafka',
#     'topic' = 'StockStream',
#     'properties.bootstrap.servers' = 'kafka:9092',
#     'properties.group.id' = 'StockStream',
#     'scan.startup.mode' = 'latest-offset',
#     'format' = 'json'
#     )
# """

# # execute DDL statement to create the source table 
# t_env.execute_sql(source_ddl)

# # retrieve the source table
# source_table = t_env.from_path('nifty_processed')
# source_table.print_schema()

# # SQL query to select all columns from table
# sql_query = "SELECT * FROM nifty_processed"
# result_table = t_env.sql_query(sql_query)
# result_table.execute().print()
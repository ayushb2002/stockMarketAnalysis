from pyflink.table import *
from pyflink.table.catalog import HiveCatalog

# creating table environment
env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)

# specify connector to kafka
# t_env.get_config().get_configuration().set_string(
#     "pipeline.jars", 
#     "file:///home/ayush/Desktop/MajorProject/flink/flink-sql-connector-hive-3.1.3_2.12-1.17.1.jar"
# )

catalog_name = "myhive"
default_database = "default"
hive_conf_dir = "/home/hadoop/apache-hive-2.3.9-bin/conf"

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
#     'topic' = 'NiftyStream',
#     'properties.bootstrap.servers' = 'kafka:9092',
#     'properties.group.id' = 'NiftyStream',
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
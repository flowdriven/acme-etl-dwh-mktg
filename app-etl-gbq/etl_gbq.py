import os 
import pandas as pd 
import mysql.connector  
from google.oauth2 import service_account
import pandas_gbq as pdbq 
import tqdm 

user = os.environ['ROOT']
password = os.environ['ROOT_PASSWORD']
host = os.environ['HOST']
port = os.environ['PORT']
database = os.environ['DATABASE'] 

secret = os.environ['SECRET']
dataset = os.environ['DATASET']
projectid = os.environ['PROJECT_ID']
credentials = service_account.Credentials.from_service_account_file('./' + secret,)

qry_all_tables = "Select table_name from information_schema.tables where table_schema = '{}'".format(database)

def get_connection():
    config = {
        'user': user,
        'password': password,
        'host': host,
        'database': database,
        #'raise_on_warnings': True, 
        'use_pure': True
    }
    return mysql.connector.connect(**config)

def get_tables(table_name, connection):
    qry_extraction = 'select * from ' + table_name
    df_table_data = pd.read_sql(qry_extraction, connection)
    return df_table_data

def transform_data(df_table_data):
    """ convert dates to string to prevent conflict with pandas-gbq """
    object_cols = df_table_data.select_dtypes(include=['object']).columns
    for column in object_cols:
        dtype = str(type(df_table_data[column].values[0]))
        if dtype == "<class 'datetime.date'>":
            df_table_data[column] = df_table_data[column].map(lambda x: str(x))
    return df_table_data

def load_to_gbq(table_name, df_table_data):
    full_table_name_bg = "{}.{}.{}".format(projectid,dataset,table_name)
    print(f"[+] Loading into table '{full_table_name_bg}': ")
    pdbq.to_gbq(
        df_table_data,
        destination_table=full_table_name_bg, 
        project_id=projectid,
        if_exists="replace", 
        credentials=credentials
    ) 
    qry_count = "SELECT COUNT(*) FROM {}".format(full_table_name_bg)
    df_result = pdbq.read_gbq(qry_count, project_id=projectid, credentials=credentials)
    rec_count = df_result.iloc[0, 0]
    print(f"[+] Successfully imported {rec_count} records into table '{full_table_name_bg}'") 

def main(): 
    try:
        connection = get_connection()
        
        df_tables = pd.read_sql(qry_all_tables, connection, parse_dates={'Date': {'format': '%Y-%m-%d'}})
        
        for table in df_tables.TABLE_NAME:
            table_name = table 

            # Extract table data from MySQL
            df_table_data = get_tables(table_name, connection)
            
            # Transform data from table
            df_table_data = transform_data(df_table_data)
            print(f"[+] Data exported from table '{table_name}' and cleaned") 

            # Import data into BigQuery 
            load_to_gbq(table_name, df_table_data)

        connection.close()

    except Exception as ex:
        connection.close()
        print(str(ex)) 
  
if __name__ == '__main__':
    main()
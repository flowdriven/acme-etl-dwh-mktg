import os
import glob 
import pandas as pd 
import mysql.connector
from sqlalchemy import create_engine   
from sqlalchemy import func, select, text 
from pathlib import Path 
  
user = os.environ['ROOT']
password = os.environ['ROOT_PASSWORD']
host = os.environ['HOST']
port = os.environ['PORT']
database = os.environ['DATABASE'] 
data_directory = os.environ['DATA_DIRECTORY'] 

def get_connection():
    db_url = "mysql+mysqlconnector://{USER}:{PWD}@{HOST}:{PORT}/{DBNAME}"
    db_url = db_url.format(
        USER = user,
        PWD = password,
        HOST = host,
        PORT = port,
        DBNAME = database
    )
    return create_engine(db_url, echo=False)

def load_files(engine):
    for filename in sorted(glob.glob('./' + data_directory + '/*csv')):
        file_path = Path(filename)
        table_name = file_path.stem
        print(f"[+] Dataset found for table: {table_name}")

        df = pd.read_csv(filename) 

        try: 
            with engine.connect() as connection: 
                df.to_sql(name=table_name,if_exists='append',con=connection,index=False) 
                connection.commit()                
 
        except Exception as e:
            print(f"[-] Import of table '{table_name}' error: {e}")
        
        with engine.connect() as connection: 
            result = connection.execute(select(func.count("*")).select_from(text(table_name))).scalar()
            print(f"[+] Load executed in table: {table_name} - Record count: {result}")
            
def main():
    try:
        engine = get_connection()
        
        print(f"[+] db engine configured as: '{engine}'")
        
        load_files(engine) 

    except Exception as ex:
        print("[-] Connection could not be made due to the following error: \n", ex) 
  
if __name__ == '__main__':
    main()
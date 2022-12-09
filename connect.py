
import pandas as pd
import psycopg2
from   config import config  


def sql(command) :
   
    conn = None
    try:
        
        params = config()
        
        # print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        conn.autocommit = True
		
        cur = conn.cursor()
        
        cur.execute(command)
        result = pd.DataFrame (cur.fetchall() )
         
	 
        cur.close()
        
        return result 
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            # print('Database connection closed.')


import psycopg
from psycopg.rows import dict_row


try:
    conn = psycopg.connect(host='localhost',
                            dbname='python_api_dev_prod_db', 
                            user='postgres', 
                        password='Kara@123',
                            port=5432,
                            row_factory=dict_row)
    
    cur = conn.cursor()
    cur.execute('''SELECT * FROM posts''')
    
    print(cur.fetchall())
    print()
    print(cur.fetchall())





    conn.commit()
    cur.close()
    conn.close()


except:
    print("db not working")










import psycopg2

def create_tables():
    
    command= """
        CREATE TABLE tweets (
            dni BIGINT,
            nombre TEXT,
            user_id BIGINT,
            tweet_id BIGINT,
            created_at_raw TEXT,
            tweett_text TEXT,
            created_timestamp TIMESTAMP,
            created_date DATE
        )
        """

    conn = None
    try:
        # conexion
        conn = psycopg2.connect(
                host="datosincorruptibles.c6gg6kroo2es.us-east-2.rds.amazonaws.com",
                database="Elecciones2020_v2",
                user="roleA",
                password="B8HNzDwS1WEWjf")
        cur = conn.cursor()
        
        cur.execute(command)
        
        cur.close()
        
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
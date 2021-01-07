import psycopg2

def create_tables():
    
    command= """
        CREATE TABLE usuarios_twitter (
            dni BIGINT,
            nombre TEXT,
            user_id BIGINT,
            created_at TEXT,
            user_name TEXT,
            user_screen_name TEXT,
            user_email TEXT,
            user_favourites_count INT,
            user_followers_counts BIGINT,
            user_following BOOLEAN,
            user_statuses_counts INT
        )
        """
    conn = None
    try:
        
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
import psycopg2
import pandas
import os



def load_data():
    handles = pandas.read_csv('twitter.csv')

    for index, row in handles.iterrows():
                       
            screen_name =  row['twitter']
            if os.path.isfile(f'{screen_name}_details.csv'):

                values = pandas.read_csv(f'{screen_name}_details.csv')
                
                command= """
                    INSERT INTO usuarios_twitter 
                    VALUES('"""+ str(values.iloc[0]['dni'])+"'"+','+"'"+str(values.iloc[0]['nombre'])+"'"+','+"'"+ str(values.iloc[0]['user_id'])+"'"+','+"'"+ str(values.iloc[0]['created_at'])+"'"+','+"'"+str(values.iloc[0]['user_name'])+"'"+','+"'"+str(values.iloc[0]['user_screen_name'])+"'"+','+"'"+str(values.iloc[0]['user_email'])+"'"+','+"'"+str(values.iloc[0]['user_favourites_count'])+"'"+','+"'"+str(values.iloc[0]['user_followers_counts'])+"'"+','+"'"+str(values.iloc[0]['user_following'])+"'"+','+"'"+str(values.iloc[0]['user_statuses_counts'])+"""')
                    """

                conn = None
                try:
                    
                    conn = psycopg2.connect(
                            host="datosincorruptibles.c6gg6kroo2es.us-east-2.rds.amazonaws.com",
                            database="Elecciones2020_v2",
                            user="roleA",
                            password="B8HNzDwS1WEWjf")
                    cur = conn.cursor()
                    cur = conn.cursor()
                    
                    cur.execute(command)
                    
                    cur.close()
                    
                    conn.commit()
                    print("row added")
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                finally:
                    if conn is not None:
                        conn.close()


if __name__ == '__main__':
    load_data()
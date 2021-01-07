from sqlalchemy import create_engine
import psycopg2 
import pandas
import io
import os
from datetime import datetime

def load_data():
    """
    Esta funcion toma los screen_names, busca un archivo con ese nombre especifico y luego actualiza la data de la tabla de tweets con la data del archivo
    """
    #este call tiene toda la data para hacer la conexion 
    engine = create_engine('postgresql+psycopg2://roleA:B8HNzDwS1WEWjf@datosincorruptibles.c6gg6kroo2es.us-east-2.rds.amazonaws.com:5432/Elecciones2020_v2')

    #cargamos la data de los screen_names
    handles = pandas.read_csv('twitter.csv')
    fails = []
    for index, row in handles.iterrows():
                                   
            screen_name =  row['twitter']
            # buscamos el archivo e.g FSagasti_tweets.csv
            if os.path.isfile(f'{screen_name}_tweets.csv'):
                
                print("doing" + screen_name)

                #leemos la data de tweets
                values = pandas.read_csv(f'{screen_name}_tweets.csv')
                #las columnas hashtags y mentioned users son listas. Podriamos subirlas a postgresql como texto, pero creo que mejor seria tener una tabla separada
                #por el momento no se estan subiendo, pero la data esta en el csv
                values = values.drop(columns=['hashtags','mentioned_users'])

                #parseamos la data de tiempo para que este en formato correcto
                values['created_timestamp'] = values.apply(lambda row: datetime.strptime(row[4], '%a %b %d %H:%M:%S +%f %Y'),axis=1)
                values['created_date'] = values.apply(lambda row: row[6].replace(hour=0,minute=0,second=0),axis = 1)
                 
                #hacemos la conexion  
                conn = engine.raw_connection()
                cur = conn.cursor()
                
                # preparamos la data para subir, esto genera un csv temporal que se elimina al cumplir el paso
                output = io.StringIO()
                values.to_csv(output, sep='\t', header=False, index=False)
                output.seek(0)
                contents = output.getvalue()
                try:
                    # subimos la data
                    cur.copy_from(output, 'tweets', null="", sep="\t") 
                    conn.commit()
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                    fails.append(screen_name)

                print(screen_name + " actualizado" )


if __name__ == '__main__':
    load_data()
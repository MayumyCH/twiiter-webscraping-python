import twitter
import csv
import os
import pandas   

keys = {'consumer_key':'key',
        'consumer_secret':'key',
        'access_token':'key',
        'access_token_secret':'key'}

handles = pandas.read_csv('twitter.csv')

def get_all_tweets(screen_names, keys):

     """
     Genera dos csv por usuario. Uno conteniendo todos los tweets, y otro con la informacion de la cuenta
     Requiere de un set de llaves de twitter y un csv conteniendo el nombre y el twitter handle del candidato     
     """

    #accedemos a twitter
    api = twitter.Api(consumer_key= keys['consumer_key'],
                  consumer_secret= keys['consumer_secret'],
                  access_token_key= keys['access_token'],
                  access_token_secret= keys['access_token_secret'],
                  tweet_mode='extended')
    
    
    
    #inicializamos la lista para guardar los tweets.
    #screen_names contiene todos los nombres y handles de los usuarios
    for index, row in screen_names.iterrows():
        alltweets = []  
        
        screen_name =  row['twitter']
        #si ya existe el csv, pasamos al siguiente usuario
        if os.path.isfile(f'{screen_name}_tweets.csv'):
            print("passing")
            pass
        else: 
           #pedimos los tweets de un usuario, el limite es 200
            try:
                new_tweets = api.GetUserTimeline(screen_name = screen_name,count=200)
                alltweets.extend(new_tweets)
                
                #guardamos el id del ultimo tweet menos 1
                oldest = alltweets[-1].id - 1
                
                #usamos ese id para buscar los tweets previos a los ultimos 200, y asi repetimos hasta que new_tweets tiene 0 tweets.
                while len(new_tweets) > 0:
                    print(f"Buscando tweets previos a {oldest}")
                    
                    #usamos el parametro max_id para evitar duplicados
                    new_tweets = api.GetUserTimeline(screen_name =  screen_name,count=200,max_id=oldest)
                    
                    alltweets.extend(new_tweets)
                    
                    #actualizamos el ultimo id
                    oldest = alltweets[-1].id - 1
                    
                    print(f"...{len(alltweets)} tweets descargados")
                
                #convertimos la data en una linea para el csv.
                #tenemos que hacer el strip de caracteres porque sino sale un error al subir la data a postgres. este: psycopg2.errors.BadCopyFileFormat: literal carriage return found in data
                

                outtweets = [[row['dni'],row['nombre_completo'],tweet.user.id,tweet.id_str, tweet.created_at, r"""{}""".format(tweet.full_text.replace('\n',' ').replace('\r',' ').rstrip("\r\n")) , tweet.hashtags, tweet.user_mentions] for tweet in alltweets]

                #descargamos la data de la cuenta
                user = api.GetUser(screen_name=screen_name)

                #creamos la data para el csv
                user_details = [row['dni'],row['nombre_completo'], user.id, user.created_at, user.name, user.screen_name, user.email, user.favourites_count,user.followers_count,user.following, user.statuses_count]
                
                #se crean los csv
                with open(f'{screen_name}_tweets.csv', 'w', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["dni","nombre","user","tweet_id","created_at","text","hashtags","mentioned_users"])
                    writer.writerows(outtweets)
                f.close()
                    
                with open(f'{screen_name}_details.csv', 'w', encoding='utf-8') as f2:
                    writer = csv.writer(f2)
                    writer.writerow(["dni","nombre","user_id","created_at","user_name","user_screen_name","user_email","user_favourites_count","user_followers_counts","user_following","user_statuses_counts"])
                    writer.writerow(user_details)
                
                pass
            except Exception as e:
                print(e)


if __name__ == '__main__':

    #leemos el csv 
    handles = pandas.read_csv('twitter.csv')

    get_all_tweets(handles,keys,directory)
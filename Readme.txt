Readme

#Scrape de twitter:

twitter_app.py

Este script necesita de un csv que contenga el nombre, dni y nombre de usuario de cada candidato. 

El script genera dos csv por candidato, uno que contiene todos sus tweets y otro con la data sobre la cuenta.

#Postgres

Hay 4 scripts relacionados a postgres, 2 para la data de usuario y 2 para la data de tweets. Un script genera la tabla y el otro lee los csvs y sube la data a la tabla


# Pasos siguientes

1. Definir como se va a resumir la data de los tweets  
    - e.g si el usuario tweeteo durante las protetast (numero de tweets entre 7 nov y 20 nov)
    - cuanto twittea a la semana
    - hace cuanto esta activo
    - si seguidor o lider (tweets originales vs retweets)


2. Crear una score de cercania entre usuarios para poder realizar el analisis de redes
    - E.g cantidad o % de retweets a un usuario 
    - e.g cantidad de followers compartidos
    - uso de hashtags
    - la manera en como calculamos este score depende de nosotros, hay varios ejemplos en google
        - https://towardsdatascience.com/generating-twitter-ego-networks-detecting-ego-communities-93897883d255
        - https://medium.com/future-vision/visualizing-twitter-interactions-with-networkx-a391da239af5
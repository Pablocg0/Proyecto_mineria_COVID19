from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
import json



# HOST hace referencia a la base de datos instalada en la computadora
HOST = 'mongodb://localhost/'
# MongoClient genera un cliente con el HOST que le determinamos
client = MongoClient(HOST)
# Se determina una base de datos llamada 'tesis' para el cliente
# Cambiar 'tesis' por el nombre de la base de datos
db = client.mujeres9m



def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

def downloadData():
    counter = 1
    menciones = pd.DataFrame()
    hasht = pd.DataFrame()
    full_data = pd.DataFrame()
    for tweet in db.mujeres.find():
        if counter <= 100:
            texto = tweet['text']
            user = tweet['user']['screen_name']
            lugar = tweet['place']['full_name'].split(",")
            if len(lugar) <2:
                lugar.append('México')
            mentions = tweet['entities']['user_mentions']
            for xs in mentions:
                dic_menc = {'mencion': [xs['screen_name']],'municipio':[lugar[0]],'estado':[lugar[1]]}
                menciones = pd.concat([menciones, pd.DataFrame(dic_menc)], axis=0)
            hashtags = tweet['entities']['hashtags']
            for ys in hashtags:
                dic_hasht = {'hashtag':[ys['text']],'municipio':[lugar[0]],'estado':[lugar[1]]}
                hasht = pd.concat([hasht, pd.DataFrame(dic_hasht)], axis=0)
            try:
                texto = tweet['extended_tweet']['full_text']
            except:
                pass
            dataDic = {'usuario':[user], 'texto':[deEmojify(texto)],'municipio':[lugar[0]],'estado':[lugar[1]]}
            data = pd.DataFrame(dataDic)
            full_data = pd.concat([full_data,data], axis=0)
            counter += 1
        else:
            break
    full_data = full_data.reset_index(drop=True)
    return (full_data,menciones,hasht)

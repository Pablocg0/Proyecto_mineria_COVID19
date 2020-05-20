from pymongo import MongoClient
import pandas as pd
from datetime import datetime, timedelta, timezone
import pytz
from unicodedata import normalize
import metrics as mt


MONGO_HOST = "132.247.22.53"
MONGO_PORT = 27017
MONGO_DB = "twitterdb"
MONGO_USER = "ConsultaTwitter"
MONGO_PASS = "$Con$ulT@C0V1D"

con = MongoClient(MONGO_HOST, MONGO_PORT)
db = con[MONGO_DB]
db.authenticate(MONGO_USER, MONGO_PASS)

tz = pytz.timezone('America/Mexico_City')
today = datetime.now(tz=tz)
today_minus = today - timedelta(days=30)
ficticia = today - timedelta(days=29)
ficticia = ficticia + timedelta(hours=4)
print(ficticia)
print(today)
print(today_minus)
#system.out


def convertDate(date):
    return datetime.strptime(date, '%a %b %d %H:%M:%S %z %Y').astimezone(tz)


def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('utf-8')


def downloadData(filtro):
    menciones = pd.DataFrame()
    hasht = pd.DataFrame()
    full_data = pd.DataFrame()
    for tweet in db.tweetsMexico.find():
        fecha = convertDate(tweet['created_at'])
        print(fecha)
        #system.out
        if fecha > today_minus and fecha < ficticia:
            print(fecha)
            texto = tweet['text']
            try:
                texto = tweet['extended_tweet']['full_text']
            except:
                pass
            if mt.etiqueta_txt(texto, filtro):
                user = tweet['user']['screen_name']
                lugar = tweet['place']['full_name'].split(",")
                ubicacion = tweet['place']['full_name']
                if len(lugar) < 2:
                    lugar.append('México')
                mentions = tweet['entities']['user_mentions']
                for xs in mentions:
                    dic_menc = {'mencion': [xs['screen_name']], 'full_place': [ubicacion]}
                    menciones = pd.concat([menciones, pd.DataFrame(dic_menc)], axis=0)
                hashtags = tweet['entities']['hashtags']
                for ys in hashtags:
                    dic_hasht = {'hashtag': [ys['text']],  'full_place': [ubicacion]}
                    hasht = pd.concat([hasht, pd.DataFrame(dic_hasht)], axis=0)
                trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
                texto = normalize('NFKC', normalize('NFKD', texto).translate(trans_tab))
                dataDic = {'usuario': [user], 'texto': [deEmojify(texto).replace('\n', ' ')],  'full_place': [ubicacion]}
                data = pd.DataFrame(dataDic)
                full_data = pd.concat([full_data, data], axis=0)
        else:
            print('nada')
            full_data = full_data.reset_index(drop=True)
            menciones = menciones.reset_index(drop=True)
            hasht = hasht.reset_index(drop=True)
            return (full_data, menciones, hasht)
    menciones = menciones.reset_index(drop=True)
    hasht = hasht.reset_index(drop=True)
    full_data = full_data.reset_index(drop=True)
    return (full_data, menciones, hasht)

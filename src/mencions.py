import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
import re
# import matplotlib.pyplot as plt
import operator
import collections


def Principal(dataframes, archivo):
    full = dataframes[0]
    ht = dataframes[2]
    mn = dataframes[1]

    estados = pd.read_csv(archivo, index_col=0)
    estados = estados.drop_duplicates(subset='PlaceJson')
    estados = estados.set_index('PlaceJson').T.to_dict('list')

    ht = CambiaEstado(ht, estados)
    mn = CambiaEstado(mn, estados)
    # full = CambiaEstado(full, estados)

    iterar = ['Ciudad de México', 'Campeche', 'Puebla', 'Estado de México',
              'Veracruz de Ignacio de la Llave', 'Hidalgo', 'Sinaloa',
              'Nuevo León', 'Quintana Roo', 'Jalisco', 'Coahuila de Zaragoza',
              'San Luis Potosí', 'Tamaulipas', 'Querétaro', 'Guanajuato',
              'Yucatán', 'Tabasco', 'Baja California', 'Oaxaca',
              'Sonora', 'Nayarit', 'Morelos', 'Durango',
              'Guerrero', 'Chihuahua', 'Michoacán de Ocampo', 'Chiapas',
              'Aguascalientes', 'Zacatecas', 'Tlaxcala', 'Baja California Sur',
              'Colima', 'Otro']

    salida = []

    for est in iterar:

        full_aux = CreaDFaux(full, est)
        mn_aux = CreaDFaux(mn, est)
        ht_aux = CreaDFaux(ht, est)

        user = extract_user(full_aux)
        arroba = extract_arroba(mn_aux)
        hashtag = extract_hashtag(ht_aux)

        aparicion_hash, hashs = generaLista(hashtag)
        aparicion_arroba, arrobas = generaLista(arroba)
        aparicion_usuario, usuarios = generaLista(user)
        # aparicion_place, place= generaLista(place)
        if est == 'Veracruz de Ignacio de la Llave':

            salida.append(['Veracruz', hashs[:3], aparicion_hash[:3],
                           arrobas[:3], aparicion_arroba[:3],
                          usuarios[:3], aparicion_usuario[:3]])
        else:
            salida.append([est, hashs[:3], aparicion_hash[:3],
                           arrobas[:3], aparicion_arroba[:3],
                           usuarios[:3], aparicion_usuario[:3]])

    df_salida = pd.DataFrame(data=salida)

    df_salida.columns = ['Estado',
                         'Hashtag', 'Num_Hash',
                         'Mencion', 'Num_mencion',
                         'Usuario_Activo', 'Num_Usr']
    return df_salida


def CambiaEstado(df, estados):
    edos = []
    # column=df.columns[-1]
    for i in range(len(df[df.columns[-1]])):
        edo = df[df.columns[-1]][i]
        """
        try:
            if len(estados[edo][0])>3:
                edos.append(estados[edo][0])
            else:
                edos.append('Otro')
        except:
            edos.append('Otros')
        """
        try:
            if estados[edo][0] != 'nan':
                edos.append(estados[edo][0])
            else:
                edos.append('Otro')
        except KeyError:
            edos.append('Otro')
    df['Estado'] = edos
    return df


def extract_user(df2):
    """ Esta función extrae los elementos de cada campo de interés
    Regresa una lista con todos los elementos extraídos"""
    user = []
    # arroba=[]
    # hashtag=[]

    for i in range(len(df2.usuario)):
        user.append(df2.usuario[i])
    """

        for j in range(len(df2.entities[i]['user_mentions'])):
            if  df2.entities[i]['user_mentions'][j]['screen_name'] != '':
                arroba.append(df2.entities[i]['user_mentions'][j]['screen_name'])

        for j in range(len(df2.entities[i]['hashtags'])):
            if df2.entities[i]['hashtags'][j]['text']!= '':
                hashtag.append(df2.entities[i]['hashtags'][j]['text'])


    hashtag=[i.lower() for i in hashtag]
    """
    return user  # , arroba, hashtag


def extract_arroba(df2):
    arroba = []

    for i in range(len(df2.mencion)):
        arroba.append(df2.mencion[i])

    return arroba


def extract_hashtag(df2):
    hashtag = []

    for i in range(len(df2.hashtag)):
        hashtag.append(df2.hashtag[i])

    hashtag = [i.lower() for i in hashtag]

    return hashtag


def generaLista(user):
    """
    Esta función recibe la lista de interes, cuenta los elementos únicos.
    Devuelve dos listas, una de nombre de elemento y la otra de cantidad de apariciones
    """

    if len(user) != 0:
        lista_users = collections.Counter(user)
        lista_users = sorted(lista_users.items(), key=operator.itemgetter(1), reverse=True)
        usuario, aparicion_usuario = map(list, zip(*lista_users))
        return aparicion_usuario, usuario
    else:
        return [0], ['Null']


def CreaDFaux(df, est):
    index = df['Estado'] == est
    dfaux = df[index]
    dfaux = dfaux.reset_index(drop=True)
    return dfaux

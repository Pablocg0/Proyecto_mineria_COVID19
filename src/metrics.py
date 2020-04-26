%matplotlib inline
import numpy as np
import seaborn as sns
from downTweets import downloadData as dwt
import re
import pandas as pd

'''
Funcion para obten de un txt texto y quitar emojis
return una lista de terminos o de textos
'''
def dataImport(filename):
    info = []
    for xs in filename:
        data = open(xs)
        for r in data:
            r = r.replace('\n', '')
            r = re.sub('https\W*t.co/\w*','',r)
            info.append(r.encode('ascii', 'ignore').decode('ascii'))
    return info

'''
Funcion que etiqueta apartir de una lista de terminos
El dataFrame debe contener una columa de nombre texto
1 si el termino aparece 0 en otro caso
return un el dataFrame original con una columna etiqueta
'''
def etiqueta(data, etiqueta):
    data_text = data['texto'].tolist()
    list_et = []
    val = -1
    for xs in data_text:
        val = -1
        for ys in etiqueta:
            if len(re.findall(ys, xs)) > 0:
                val = 1
                break
            else:
                val = 0
        list_et.append(val)
    eti_df = pd.DataFrame(list_et, columns=['etiqueta'])
    return pd.concat([data,eti_df], axis=1)


'''
Funcion que apartir de una lista de texto y una lista de terminos
saca el numero de apariciones de los terminos
return dataFrame con los terminos y su pertinente numero de apariciones
'''
def numApariciones(texto, terminos):
    numRepeticiones = []
    it = 0
    for xs in terminos:
        it = 0
        for ys in texto:
            it += len(re.findall(xs, ys))
        numRepeticiones.append(it)


    terminos_df = pd.DataFrame(terminos, columns=['terminos'])
    aparaciones_df = pd.DataFrame(numRepeticiones, columns=['#Repeticiones'])
    return pd.concat([terminos_df, aparaciones_df], axis = 1)


'''
Funcion para hacer una  grafica de radar
apartir de un dataFrame con dos columna de nombre terminos y #Repeticiones
'''
def grafica_radar(data, termino):
    labels=np.array(data['terminos'])
    stats= data['#Repeticiones'].values

    angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)

    stats=np.concatenate((stats,[stats[0]]))
    angles=np.concatenate((angles,[angles[0]]))

    fig= plt.figure(figsize=(22.2, 11.4))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, stats, 'o-', linewidth=2)
    ax.fill(angles, stats, alpha=0.25)
    ax.set_thetagrids(angles * 180/np.pi, labels)
    ax.set_title(termino + ' mas mencionados')
    ax.grid(True)
    plt.show()


menciones = dataImport(['../data/diccionarios/cod.txt'])
dataFull = dwt()
data = etiqueta(dataFull[0], menciones)
print(data)

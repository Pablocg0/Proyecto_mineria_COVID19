import metrics as mt
import downTweets as dt
import data_json as dj
import mencions as mn


sintomas = mt.dataImport(['../data/diccionarios/sintomas.txt'])
mentales = mt.dataImport(['../data/diccionarios/mentales.txt'])
filtro = mt.dataImport(['../data/diccionarios/cod.txt'])
direccion = '../data/json/'

dataFull = dt.downloadData(filtro)
# data = mt.etiqueta(dataFull[0], filtro)
try:
    data = mt.change_edo(dataFull[0])

    dj.procesar_mapa([direccion+'Hashtags', direccion+'Menciones', direccion+'Usuarios_activos'], mn.Principal([data, dataFull[1], dataFull[2]]))
    dj.json_radar(direccion+'radar_mentales', mt.numApariciones(data, mentales))
    dj.json_radar(direccion+'radar_sintomas', mt.numApariciones(data, sintomas))
    dj.procesar_mapa2(direccion+'mapa_mentales', mt.repetcions_ed(data, mentales))
    dj.procesar_mapa2(direccion+'mapa_sintomas', mt.repetcions_ed(data, sintomas))
except:
    print('No hay tweets por procesar')

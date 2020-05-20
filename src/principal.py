import metrics as mt
import downTweets as dt
import data_json as dj
import mencions as mn


sintomas = mt.dataImport(['../data/diccionarios/sintomas.txt'])
mentales = mt.dataImport(['../data/diccionarios/mentales.txt'])
filtro = mt.dataImport(['../data/diccionarios/cod.txt'])
direccion = '../data/json/'

dataFull = dt.downloadData(filtro)
#data = mt.etiqueta(dataFull[0], filtro)
data = mt.change_edo(dataFull[0])
# dataf = data[data['etiqueta'] == 1]
# data_proc = numApariciones(data, menciones)
# print(data_proc)
dj.procesar_mapa([direccion+'Hashtags', direccion+'Menciones', direccion+'Usuarios_activos'], mn.Principal([data, dataFull[1], dataFull[2]]))
dj.json_radar(direccion+'radar_mentales', mt.numApariciones(data, mentales))
dj.json_radar(direccion+'radar_sintomas', mt.numApariciones(data, sintomas))
dj.procesar_mapa2(direccion+'mapa_mentales', mt.repetcions_ed(data, mentales))
dj.procesar_mapa2(direccion+'mapa_sintomas', mt.repetcions_ed(data, sintomas))

# try:
#     dataFull = dt.downloadData()
#     print(len(dataFull))
#     data = mt.etiqueta(dataFull[0], filtro)
#     data = data[data['etiqueta'] == 1]
#     # data_proc = numApariciones(data, menciones)
#     # print(data_proc)
#     dj.procesar_mapa(['Hashtags', 'Menciones', 'Usuarios_activos'], mn.Principal([data, dataFull[1], dataFull[2]]))
#     data = mt.change_edo(data)
#     dj.json_radar('radar_mentales', mt.numApariciones(data, mentales))
#     dj.jason_radar('radar_sintomas', mt.numApariciones(data, sintomas))
#     dj.proecesar_mapa2('mapa_mentales', mt.repetcions_ed(data, mentales))
#     dj.proecesar_mapa2('mapa_sintomas', mt.repetcions_ed(data, sintomas))
# except:
#     print('No hay tweets que procesar')

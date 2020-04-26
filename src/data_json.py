

def json_radar(nombre, data):
    f = open (nombre+".json","w")
    lines = '[ \n'
    for indice_fila, fila in data.iterrows():
        lines += '{\n \"subject\": \"'+fila['terminos']+'\", \"A\":'+str(fila['#Repeticiones'])+'\n },\n'
    lines = lines[:len(lines)-2] + '\n]'
    f.write(lines)
    f.close()

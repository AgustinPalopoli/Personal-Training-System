import os

def at(texto):
    #Acomodar texto de inputs
    try:
        texto = texto.lower()
        texto = texto.capitalize()
        texto = texto.strip()
    except:
        texto = texto
    return texto

def eliminar_imagen(modelo,index):
    for id in index:
        eliminar = modelo.objects.get(id=id)
        os.remove("plataforma/static/plataforma/imagenes/"+str(eliminar.imagen))

def agregar_modelo(modelo,index,data):
    nueva_data = modelo()
    for i in range(0,len(data)):
        setattr(nueva_data, index[i],at(data[i]))
    nueva_data.save()
    return nueva_data

def eliminar_modelo(modelo,index):
    for id in index:
        modelo.objects.filter(id=id).delete()

def eliminar_modelo_imagen(modelo,index):
    eliminar_imagen(modelo,index)
    eliminar_modelo(modelo,index)

def modificar_modelo(modelo,index,data,id):
    nueva_data = modelo.objects.get(id=id)
    for i in range(0,len(data)):
        setattr(nueva_data, index[i],at(data[i]))
    nueva_data.save()
    return nueva_data

def modificar_modelo_imagen(modelo,index,data,id):
    eliminar_imagen(modelo,id)
    nueva_data = modificar_modelo(modelo,index,data,id)
    return nueva_data


def agregar_modelo_mtm(modelo,index,data):
    nueva_data = modelo()
    for i in range(0,len(data)-1):
        setattr(nueva_data, index[i],at(data[i]))
    nueva_data.save()
    for j in range(0,len(data[-1])):
        setattr(nueva_data, index[-1],set(data[-1][j]))
    nueva_data.save()
    return nueva_data
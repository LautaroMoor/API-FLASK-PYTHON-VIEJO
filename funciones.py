import json

#Leer JSONs
with open ('jsons/usuarios.json','r',encoding="utf8") as archivoJson:
    usuarios = json.load(archivoJson)

with open ('jsons/peliculas.json','r',encoding="utf8") as archivoJson:
    peliculas = json.load(archivoJson)

with open ('jsons/directores.json','r',encoding="utf8") as archivoJson:
    directores = json.load(archivoJson)

with open ('jsons/generos.json','r',encoding="utf8") as archivoJson:
    generos = json.load(archivoJson)

with open ('jsons/comentarios.json','r',encoding="utf8") as archivoJson:
    comentarios = json.load(archivoJson)

#Pasando a JSONs
def obtenerUsuarios():
    return usuarios

def obtenerPeliculas():
    return peliculas

def obtenerDirectores():
    return directores

def obtenerGeneros():
    return generos

def obtenerComentarios():
    return comentarios

#Nuevas ID
def nuevaIdPeliculas():
    return str(int(peliculas[-1]["id"]) + 1)

def nuevoIdComentario():
    return str(int(comentarios[-1]["id"]) + 1)
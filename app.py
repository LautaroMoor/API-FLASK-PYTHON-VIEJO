from flask import Flask, jsonify, Response, request
import funciones as fc
from http import HTTPStatus
import json
from random import choice

app = Flask(__name__)

#Rutas API
@app.route("/usuario/<usuarioUI>/contrasena/<contrasenaUI>")
def getLogin(usuarioUI,contrasenaUI):
    #Obteneniendo JSONs
    usuarios = fc.obtenerUsuarios()

    for usuario in usuarios:
        if usuario['usuario'] == usuarioUI and usuario['contrasena'] == contrasenaUI and usuarioUI != '' and contrasenaUI != '':
            return str(usuario['id'])
            
    return 'Error'

@app.route("/directores")
def getDirectores():
    #Obteneniendo JSONs
    directores = fc.obtenerDirectores()
    return jsonify(directores)

@app.route("/directores/<id>")
def getDirectoresByCodigo(id):
    #Obteneniendo JSONs
    directores = fc.obtenerDirectores()
    for director in directores:
        if director['id'] == id:
            return director
    return Response("{}", status=HTTPStatus.NOT_FOUND)

@app.route("/generos")
def getGeneros():
    #Obteneniendo JSONs
    generos = fc.obtenerGeneros()
    return jsonify(generos)

@app.route("/generos/<id>")
def getGenerosByCodigo(id):
    #Obteneniendo JSONs
    generos = fc.obtenerGeneros()
    for genero in generos:
        if genero['id'] == id:
            return genero
    return Response("{}", status=HTTPStatus.NOT_FOUND)

@app.route("/peliculas/director/<id>")
def getPeliculasByDirector(id):
    #Obteneniendo JSONs
    peliculas = fc.obtenerPeliculas()

    peliculasByDirector = []

    for pelicula in peliculas:
        if pelicula["idDirector"] == id:
            peliculasByDirector.append(pelicula)
    if len(peliculasByDirector)==0:
        return jsonify('Director no encontrado')
    else:
        return jsonify(peliculasByDirector)

@app.route("/peliculas/imagen")
def getPeliculasByPortada():
    #Obteneniendo JSONs
    peliculas = fc.obtenerPeliculas()

    peliculasByPortada = []
    for pelicula in peliculas:
        if pelicula["imagen"] != '':
            peliculasByPortada.append(pelicula)
    if len(peliculasByPortada)==0:
        return jsonify("Peliculas con portada no encontradas")
    else:
        return jsonify(peliculasByPortada)

#ABM peliculas
@app.route("/peliculas")
def getPeliculas():
    #Obteneniendo JSONs
    peliculas = fc.obtenerPeliculas()
    return jsonify(peliculas)

@app.route("/peliculas/create", methods=['POST'])
def createPelicula():
    #Obteneniendo JSONs
    peliculas = fc.obtenerPeliculas()
    nuevaPelicula = request.get_json()
    id= fc.nuevaIdPeliculas()

    nuevaPelicula["id"] = id
    peliculas.append(nuevaPelicula)

    #Actualizando JSONs
    with open('jsons/peliculas.json', 'w') as archivoJson:
        json.dump(peliculas, archivoJson, indent=4)

    return 'Pelicula registrada correctamente.'

@app.route("/peliculas/save/", methods=['PUT'])
def savePelicula():
    #Obteneniendo JSONs
    peliculas = fc.obtenerPeliculas()

    nuevaPeliculaDicccionario = request.get_json()

    for pelicula in peliculas:
        if pelicula["id"] == nuevaPeliculaDicccionario["id"]:
            if nuevaPeliculaDicccionario["titulo"] != '':
                pelicula["titulo"] = nuevaPeliculaDicccionario["titulo"]
            elif nuevaPeliculaDicccionario["ano"] != '':
                pelicula["ano"] = nuevaPeliculaDicccionario["ano"]
            elif nuevaPeliculaDicccionario["idDirector"] != '':
                pelicula["idDirector"] = nuevaPeliculaDicccionario["idDirector"]
            elif nuevaPeliculaDicccionario["idGenero"] != '':
                pelicula["idGenero"] = nuevaPeliculaDicccionario["idGenero"]
            elif nuevaPeliculaDicccionario["sinopsis"] != '':
                pelicula["sinopsis"] = nuevaPeliculaDicccionario["sinopsis"]
            elif nuevaPeliculaDicccionario["imagen"] != 'no cargado':
                pelicula["imagen"] = nuevaPeliculaDicccionario["imagen"]

    #Actualizando JSONs
    with open('jsons/peliculas.json', 'w') as archivoJson:
        json.dump(peliculas, archivoJson, indent=4)

    return 'Pelicula exitosamente modificada'

@app.route("/peliculas/delete/<id>/idUsuario/<idUsuario>", methods=['DELETE'])
def deletePelicula(id, idUsuario):
    #Obteneniendo JSONs
    peliculas = fc.obtenerPeliculas()
    comentarios = fc.obtenerComentarios()
    comentariosOtrosUsuarios = False
    valor = {}

    for pelicula in peliculas:
        if pelicula["id"] == id:
            for comentarioRecorrido in pelicula["idComentarios"]:
                for comentario in comentarios:
                    if comentarioRecorrido == comentario["id"]  and comentario["idUsuario"] != idUsuario:
                        comentariosOtrosUsuarios = True
        if comentariosOtrosUsuarios == False and pelicula["id"] == id:
            valor = pelicula 
            for peliculaIdComentarios in valor["idComentarios"]:
                for comentario in comentarios:
                    if comentario['id'] == peliculaIdComentarios:
                        comentarios.remove(comentario)

    if comentariosOtrosUsuarios == True:
        return 'Borrado no exitoso, tiene comentarios de otros usuarios o no se pudo eliminar correctamente'
    else:
        peliculas.remove(valor)
        #Actualizando JSONs
        with open('jsons/peliculas.json', 'w') as archivoJson:
            json.dump(peliculas, archivoJson, indent=4)
        with open('jsons/comentarios.json', 'w') as archivoJson:
            json.dump(comentarios, archivoJson, indent=4)
        return 'Borrado exitoso'

@app.route("/peliculas/<id>")
def getPeliculaByCodigo(id):
    #Obteneniendo JSONs
    peliculas = fc.obtenerPeliculas()

    for pelicula in peliculas:
        if pelicula["id"] == id:
            return jsonify(pelicula)
    return Response("{}", status=HTTPStatus.NOT_FOUND)

@app.route("/ultimasdiezpeliculas")
def getUltimas10Peliculas():
    #Obteneniendo JSONs
    peliculas = fc.obtenerPeliculas()
    ultimas10Peliculas = []
    contador = 0

    for pelicula in reversed(peliculas):
        contador = contador + 1
        ultimas10Peliculas.append(pelicula)
        if contador == 10:
            break

    if len(ultimas10Peliculas) == 0:
        return jsonify('No hay peliculas')
    else:
        return jsonify(ultimas10Peliculas)

@app.route("/pelicularandom")
def getPeliculaRandom():
    peliculas = fc.obtenerPeliculas()
    return choice(peliculas)

#ABM Comentarios
@app.route("/comentario/create/idPelicula/<idPelicula>", methods=['POST'])
def createComentarios(idPelicula):
    #Obteneniendo JSONs
    comentarios = fc.obtenerComentarios()
    peliculas = fc.obtenerPeliculas()
    id = fc.nuevoIdComentario()

    comentarioNuevo = request.get_json()
    comentarioNuevo["id"] = id
    comentarios.append(comentarioNuevo)
    
    for pelicula in peliculas:
        if pelicula['id'] == idPelicula:
            pelicula['idComentarios'].append(id)

    #Actulizando jsons
    with open('jsons/comentarios.json', 'w') as archivoJson:
        json.dump(comentarios, archivoJson, indent=4)
    with open('jsons/peliculas.json', 'w') as archivoJson:
        json.dump(peliculas, archivoJson, indent=4)

    return 'Creacion de comentario exitosa'

@app.route("/comentario/idUsuario/<idUsuario>/delete/<id>", methods=['DELETE'])
def deleteComentarios(id,idUsuario):
    #Obteneniendo JSONs
    comentarios = fc.obtenerComentarios()
    peliculas = fc.obtenerPeliculas()
    borrado = False

    for comentario in comentarios:
        if comentario["idUsuario"] == idUsuario and comentario["id"] == id:
            comentarios.remove(comentario)
            for pelicula in peliculas:
                for comentarioRecorrido in pelicula["idComentarios"]:
                    if comentarioRecorrido == id:
                        borrado = True
                        pelicula["idComentarios"].remove(comentarioRecorrido)

    #Actulizando JSONs
    with open('jsons/comentarios.json', 'w') as archivoJson:
        json.dump(comentarios, archivoJson, indent=4)
    with open('jsons/peliculas.json', 'w') as archivoJson:
        json.dump(peliculas, archivoJson, indent=4)

    if borrado:
        return 'Borrado con exito'
    else:
        return 'Borrado sin exito'

@app.route("/comentario/idUsuario/<idUsuario>")
def getComentariosByUsuario(idUsuario):
    #Obteneniendo JSONs
    comentarios = fc.obtenerComentarios()

    listaComentariosUsuario = []

    for comentario in comentarios:
        if comentario["idUsuario"] == idUsuario:
            listaComentariosUsuario.append(comentario)

    return jsonify(listaComentariosUsuario)

@app.route("/comentario/save", methods=['PUT'])
def saveComentarios():
    #Obteneniendo JSONs
    comentarios = fc.obtenerComentarios()
    
    comentarioNuevoLista = request.get_json()

    for comentario in comentarios:
        if comentario['id'] == comentarioNuevoLista['id'] and comentario['idUsuario'] == comentarioNuevoLista['idUsuario']:
            comentario['comentario'] = comentarioNuevoLista['comentario']

    #Actulizando JSONs
    with open('jsons/comentarios.json', 'w') as archivoJson:
        json.dump(comentarios, archivoJson, indent=4)

    return 'Modificacion con exito'

@app.route("/comentario/<id>")
def getComentariosById(id):
    comentarios = fc.obtenerComentarios()

    for comentario in comentarios:
        if comentario['id'] == id:
            return jsonify(comentario)

@app.route("/peliculas/<idPelicula>/comentarios/")
def getComentarios(idPelicula):
    #Obteneniendo JSONs
    comentarios = fc.obtenerComentarios()
    peliculas = fc.obtenerPeliculas()

    listaComentarios = []

    for pelicula in peliculas:
        if pelicula['id'] == idPelicula:
            for comentarioRecorrido in pelicula["idComentarios"]:
                for comentario in comentarios:
                    if comentario['id'] == comentarioRecorrido:
                        listaComentarios.append(comentario)
                return jsonify(listaComentarios)

    return Response("{}", status=HTTPStatus.NOT_FOUND)

if __name__ == "__name__": 
	app.run(debug = True, port=5000)
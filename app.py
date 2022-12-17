from flask import Flask, jsonify, Response
from requests import Timeout
import funciones as fc
from http import HTTPStatus
import json

app = Flask(__name__)

#Rutas API
@app.route("/usuario/<usuarioUI>/contrasena/<contrasenaUI>")
def getLogin(usuarioUI,contrasenaUI):
    #Obteneniendo JSONs
    usuarios = fc.obtenerUsuarios()

    for usuario in usuarios:
        if usuario['usuario'] == usuarioUI and usuario['contrasena'] == contrasenaUI:
            return "1"
            
    return "0"

@app.route("/directores")
def getDirectores():
    #Obteneniendo JSONs
    directores = fc.obtenerDirectores()
    return jsonify(directores)

@app.route("/generos")
def getGeneros():
    #Obteneniendo JSONs
    generos = fc.obtenerGeneros()
    return jsonify(generos)

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

@app.route("/peliculas/create/titulo/<titulo>/ano/<ano>/idDirector/<idDirector>/idGenero/<idGenero>/sinopsis/<sinopsis>/imagen/<imagen>", methods=['POST'])
def createPelicula(titulo, ano, idDirector, idGenero, sinopsis, imagen):
    #Obteneniendo JSONs
    peliculas = fc.obtenerPeliculas()

    id = fc.nuevaIdPeliculas()

    nuevaPelicula={"id":id,"titulo":titulo, "ano":ano, "idDirector":idDirector, "idGenero":idGenero, "sinopsis":sinopsis, "imagen":imagen, "idComentarios":[]}
    peliculas.append(nuevaPelicula)

    #Actualizando JSONs
    with open('jsons/peliculas.json', 'w') as archivoJson:
        json.dump(peliculas, archivoJson, indent=4)

    return jsonify(peliculas)

@app.route("/peliculas/save/<id>/titulo/<titulo>/ano/<ano>/idDirector/<idDirector>/sinopsis/<sinopsis>", methods=['PUT'])
def savePelicula(id,titulo,ano,idDirector,sinopsis):
    #Obteneniendo JSONs
    peliculas = fc.obtenerPeliculas()

    for pelicula in peliculas:
        if pelicula["id"] == id:
            pelicula["titulo"] = titulo
            pelicula["ano"] = ano
            pelicula["idDirector"] = idDirector
            pelicula["sinopsis"] = sinopsis

    #Actualizando JSONs
    with open('jsons/peliculas.json', 'w') as archivoJson:
        json.dump(peliculas, archivoJson, indent=4)

    return jsonify(peliculas)

@app.route("/peliculas/delete/<id>", methods=['DELETE'])
def deletePelicula(id):
    #Obteneniendo JSONs
    peliculas = fc.obtenerPeliculas()

    for pelicula in peliculas:
        if pelicula["id"] == id:
            peliculas.remove(pelicula)
            #Actualizando JSONs
            with open('jsons/peliculas.json', 'w') as archivoJson:
                json.dump(peliculas, archivoJson, indent=4)
            return jsonify(peliculas)

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

#ABM Comentarios
@app.route("/comentario/create/idPelicula/<idPelicula>/idUsuario/<idUsuario>/comentario/<comentarioNuevo>", methods=['POST'])
def createComentarios(idPelicula,idUsuario,comentarioNuevo):
    #Obteneniendo JSONs
    comentarios = fc.obtenerComentarios()
    peliculas = fc.obtenerPeliculas()

    id = fc.nuevoIdComentario()
    
    comentarioNuevo = {"id":id,"idUsuario":idUsuario,"comentario":comentarioNuevo}
    comentarios.append(comentarioNuevo)
    
    for pelicula in peliculas:
        if pelicula['id'] == idPelicula:
            pelicula['idComentarios'].append(id)

    #Actulizando jsons
    with open('jsons/comentarios.json', 'w') as archivoJson:
        json.dump(comentarios, archivoJson, indent=4)
    with open('jsons/peliculas.json', 'w') as archivoJson:
        json.dump(peliculas, archivoJson, indent=4)

    return jsonify(comentarios)

@app.route("/comentario/delete/<id>", methods=['DELETE'])
def deleteComentarios(id):
    #Obteneniendo JSONs
    comentarios = fc.obtenerComentarios()
    peliculas = fc.obtenerPeliculas()

    for comentario in comentarios:
        if comentario["id"] == id:
            comentarios.remove(comentario)

    for pelicula in peliculas:
        for comentarioRecorrido in pelicula["idComentarios"]:
            if comentarioRecorrido == id:
                pelicula["idComentarios"].remove(comentarioRecorrido)

    #Actulizando JSONs
    with open('jsons/comentarios.json', 'w') as archivoJson:
        json.dump(comentarios, archivoJson, indent=4)
    with open('jsons/peliculas.json', 'w') as archivoJson:
        json.dump(peliculas, archivoJson, indent=4)

    return jsonify(comentarios)

@app.route("/comentario/save/<id>/idUsuario/<idUsuario>/comentario/<comentarioNuevo>", methods=['PUT'])
def saveComentarios(id,idUsuario,comentarioNuevo):
    #Obteneniendo JSONs
    comentarios = fc.obtenerComentarios()
    
    for comentario in comentarios:
        if comentario['id'] == id and comentario['idUsuario'] == idUsuario:
            comentario['comentario'] = comentarioNuevo

    #Actulizando JSONs
    with open('jsons/comentarios.json', 'w') as archivoJson:
        json.dump(comentarios, archivoJson, indent=4)

    return jsonify(comentarios)


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


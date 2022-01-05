from flask import Flask, request, jsonify, Response
from flask.wrappers import Response
from flask_pymongo import PyMongo
from werkzeug.wrappers import response
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/moviegoer'
mongo= PyMongo(app)

@app.route('/comentarios', methods=['POST'])
def create_comentario():
    #Recibe la información
   titulo = request.json['titulo']
   estreno = request.json['estreno']
   descripcion = request.json['descripcion']
   comentario = request.json['comentario']

   if titulo and estreno and descripcion and comentario:
       id = mongo.db.comentarios.insert(
           {'titulo': titulo, 'estreno': estreno, 'descripcion': descripcion, 'comentario': comentario}
       )
       response ={
           'id': str(id),
            'titulo': titulo,
            'estreno': estreno,
            'descripcion' : descripcion,
            'comentario': comentario
       }
       return response
   else:
        return not_found()

   return {'message':'received'}

@app.route('/comentarios', methods=['GET'])
def get_comentario():
    comentarios = mongo.db.comentarios.find()
    response = json_util.dumps(comentarios)
    return Response(response, mimetype='application/json')

@app.route('/comentarios/<id>', methods=['GET'])
def get_comentario(id):
    comentario = mongo.db.comentarios.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(comentario)
    return Response(response, mimetype='application/json')

@app.route('/comentarios/<id>', methods=['DELETE'])
def delete_comentario(id):
    comentario = mongo.db.comentarios.delete_one({'_id': ObjectId(id)})
    response = jsonify({
        'message' : 'Review:' + id +'was Deleted Successfully',
    })
    return response

@app.route('/comentarios/<id>', methods=['PUT'])
def update_comentario(id):
    titulo = request.json['titulo']
    estreno = request.json['estreno']
    descripcion = request.json['descripcion']
    comentario = request.json['comentario']
    if titulo and estreno and descripcion and comentario:
        mongo.db.comentarios.update_one({'_id' : ObjectId(id)}, {'$set': {
           'titulo': titulo,
           'estreno': estreno,
           'descripcion': descripcion,
           'comentario': comentario
        }})
    response = jsonify({
        'message' : 'Review:' + id +'was Updated Successfully',
    })
    return response


@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message' : 'Resource Not Found:' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__ == "__name__":
    app.run(debug=True)
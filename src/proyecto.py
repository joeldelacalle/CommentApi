from distutils.command.config import config
from flask import Flask, request, jsonify, Response, Blueprint
from flask.wrappers import Response
from flask_pymongo import PyMongo
from flask_swagger_ui import get_swaggerui_blueprint
from routes import request_api
from bson import json_util
from bson.objectid import ObjectId
from flask_cors import CORS

#REQUEST_API = Blueprint('request_api', __name__)

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/moviegoer'
app.config['SWAGGER'] = {'title': 'Swagger-UI', 'universion': 2}
mongo= PyMongo(app)
CORS(app)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "PROYECTO"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

app.register_blueprint(request_api.get_blueprint())

@app.route('/comentarios', methods=['POST'])
#@REQUEST_API.route('/comentarios', methods=['POST'])
def create_comentario():
    #Recibe la información
   titulo = request.json['titulo']
   idPelicula = request.json['idPelicula']
   nomUsuario = request.json['nomUsuario']
   emailUsuario = request.json['emailUsuario']
   comentario = request.json['comentario']

   if titulo and idPelicula and nomUsuario and emailUsuario and comentario:
       id = mongo.db.comentarios.insert(
           {'titulo': titulo, 'idPelicula': str(idPelicula), 'nomUsuario': nomUsuario, 'emailUsuario': emailUsuario, 'comentario': comentario}
       )
       response ={
            'id': str(id),
            'titulo': titulo,
            'idPelicula': str(idPelicula), 
            'nomUsuario': nomUsuario,
            'emailUsuario' : emailUsuario,
            'comentario': comentario
       }
       return response
   else:
        return not_found()

   return {'message':'received'}

@app.route('/comentarios', methods=['GET'])
#@REQUEST_API.route('/comentarios', methods=['GET'])
def get_comentarios():
    comentarios = mongo.db.comentarios.find()
    response = json_util.dumps(comentarios)
    return Response(response, mimetype='application/json')

@app.route('/comentarios/<id>', methods=['GET'])
def get_comentarioPelicula(id):
    comentario = mongo.db.comentarios.find({'idPelicula': str(id)})
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
    nomUsuario = request.json['nomUsuario']
    emailUsuario = request.json['emailUsuario']
    comentario = request.json['comentario']
    if titulo and nomUsuario and emailUsuario and comentario:
        mongo.db.comentarios.update_one({'_id' : ObjectId(id)}, {'$set': {
           'titulo': titulo,
           'nomUsuario': nomUsuario,
           'emailUsuario': emailUsuario,
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
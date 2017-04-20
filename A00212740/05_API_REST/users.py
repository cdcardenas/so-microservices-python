from flask import Flask, abort, request
import json

from users_commands import get_all_users, add_user, remove_user, recently_logged, get_that_user, recently_commands

app = Flask(__name__)
api_url = '/v1.0'

@app.route(api_url+'/users',methods=['POST'])
def create_user():
  content = request.get_json(silent=True)
  username = content['username']
  password = content['password']
  if not username or not password:
    return "empty username or password", 400
  if username in get_all_users():
    return "user already exist", 400
  if add_user(username,password):
    return "user created", 201
  else:
    return "error while creating user", 400

@app.route(api_url+'/users/<string:username>',methods=['GET'])
def get_single_user(username):
 if get_that_user(username)==False:
  return "El usuario seleccionado no existe",400
 else:
  usuario= get_that_user(username)
  return json.dumps(usuario), 200

@app.route(api_url+'/users/<string:username>',methods=['POST'])
def post_infouser():
 return "HTTP 404 NOT FOUND", 404

@app.route(api_url+'/users/<string:username>',methods=['DELETE'])
def delete_single__user(username):
 if get_that_user(username)==False:
  return 'Error, el usuario no existe', 400
 else:
  remove_user(username);
  return 'OK. el usuario ha sido eliminado', 200

@app.route(api_url+'users/recently_logged',methods=['GET'])
def recent_users():
 logged = {}
 logged = recently_logged()

 if logged:
  return json.dumps(logged),200
 else:
  return "No hay usuarios recientemente logeados"

@app.route(api_url+'/users/recently_logged',methods=['POST'])
def post_recently():
 return "HTTP 404 Not Found",404

@app.route(api_url+'/users/recently_logged', methods=['DELETE'])
def delete_recently():
 return "HTTP 404 Not Found", 404

@app.route(api_url+'/users/recently_logged', methods=['PUT'])
def put_recently():
 return "HTTP 404 Not Found", 404

@app.route(api_url+'/users/<string:username>/commands', methods=['GET'])
def user_commands(username):
 if get_that_user(username)==False:
  return "HTTP 400 Not Found"
 else:
  comandos= {}
  comandos=recently_commands(username);
  return json.dumps(comandos), 200

@app.route(api_url+'/users/<string:username>/commands', methods=['POST'])
def p_ucommands():
 return "HTTP 404 NOT FOUND", 404

@app.route(api_url+'/users/<string:username>/commands', methods=['PUT'])
def put_ucommands():
 return "HTTP 404 NOT FOUND", 404

@app.route(api_url+'/users/<string:username>/commands', methods=['DELETE'])
def del_ucommands():
 return "HTTP 404 NOT FOUND", 404




@app.route(api_url+'/users',methods=['GET'])
def read_user():
  list = {}
  list["users"] = get_all_users()
  return json.dumps(list), 200

@app.route(api_url+'/users',methods=['PUT'])
def update_user():
  return "not found", 404

@app.route(api_url+'/users',methods=['DELETE'])
def delete_user():
  error = False
  for username in get_all_users():
    if not remove_user(username):
        error = True

  if error:
    return 'some users were not deleted', 400
  else:
    return 'all users were deleted', 200

if __name__ == "__main__":

  app.run(host='0.0.0.0',port=8080,debug='True')

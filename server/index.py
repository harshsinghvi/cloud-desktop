import docker

from flask import Flask, request, jsonify, render_template, session, redirect
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo,ObjectId

from pytz import timezone
from datetime import datetime

from settings import *



# Flask app config
app = Flask(__name__)
app.config["DEBUG"] = True

# database config
app.config['MONGO_URI'] = MONGODB_URI
mongo = PyMongo(app)

#CORS config
CORS(app, support_credentials=True)

# DOCKER CONFIG 
# client = docker.from_env() ## for local docker host 
client = docker.DockerClient(base_url=DOCKER_REMOTE_HOST) ## for remote docker host

# Session Properties
SESSION_DETAILS=['username','authenticated']
USERNAME = SESSION_DETAILS[0]
AUTHENCATED = SESSION_DETAILS[1]

# TZ
IST = timezone(TIME_ZONE) 

# custom functions
def auth_check(username, password):
        creds = mongo.db.find({"username":request.args['username']},{ "_id": 0, "username": 1, "password": 1 })
        if creds['username'] == request.args['username'] and creds['password'] == request.args['password']:
            session['username']=request.args['username']
            session['authenticated']='1'
            return True
        else: 
            return False

@app.route('/', methods=['GET', 'POST'])
def root():
    return redirect(FRONTEND_URL)

@cross_origin()
@app.route('/auth', method = ['POST', 'GET'])
def auth():
    if 'username' in request.args and 'password' in request.args:
        creds = mongo.db.find({"username":request.args['username']},{ "_id": 0, "username": 1, "password": 1 })
        if creds['username'] == request.args['username'] and creds['password'] == request.args['password']:
            session['username']=request.args['username']
            session['authenticated']='1'
            return "Auth OK", 200
        else: 
            return "Auth Failed check username and password", 401
    return "No Username or Password supplied in query parms.", 400

@cross_origin()
@app.route('/reset-auth', method = ['POST', 'GET'])
def reset_auth():
    if int(session[USERNAME]):
        for d in SESSION_DETAILS:
            session.pop(d, None)
        return "Rest auth Susccefull", 200
    return "Unauthenticated or Unknown Error", 400



@app.route('/hello-world',methods=['GET'])
def hello_world():
    return client.containers.run("hello-world", remove=True)

@app.route('/version',methods=['GET'])
def docker_version():
    return client.version()
@app.route('/pull-images',methods=['GET'])
def pull_images():
    temp=[]
    for image in DOCKER_IMAGES:
        try:
            temp.append(str(client.images.pull(image)))
        except docker.errors.ImageNotFound:
            temp.append(image+" : notfound")
    return {"images":temp}

@app.route('/info',methods=['GET'])
def info():
    return client.info()

@app.route('/df',methods=['GET'])
def df():
    return client.df()
@app.route('/get-container',methods=['GET'])
def get_container():
    image=DEFAULT_DOCKER_IMAGE
    if 'pass' not in request.args:
        print('no pass')
        if 'image' in request.args and request.args['image'] in DOCKER_IMAGES:
            image=request.args['image']
        container=client.containers.run(image,"--auth none",detach=True, ports={'8080': None})
    else :
        if 'image' in request.args and request.args['image'] in DOCKER_IMAGES:
            image=request.args['image']
        container=client.containers.run(image,detach=True, ports={'8080': None},environment={'PASSWORD':request.args['pass']})
    
    for i in client.df()['Containers']:
        if i['Id'] == container.id:
            break
    return {
        'container_id':container.id,
        'container_name':container.name,
        'container_ports': i['Ports'],
        'container_public_port': i['Ports'][0]['PublicPort'],
        'container_image': i['Image']
    }

@app.route('/delete-container', methods=['DELETE'])
def del_container():
    if "container_id" not in request.args:
        return "PASS THE CONTAINER ID to delete",400
    try:
            client.containers.get(request.args['container_id']).kill(),
            client.containers.get(request.args['container_id']).remove(force=True)
    except docker.errors.NotFound:
        return "Container already DELETED or container_id not vaid",400
    return {'action':"DELETE", 'container_id': request.args['container_id']},200


@app.route('/delete-containers-all',methods=['DELETE'])
def del_all_containers():
    con=client.containers.list(filters={'ancestor':DOCKER_IMAGES})
    deleted_containers={}
    for i in con:
        deleted_containers[i.name]=i.id
        i.kill()
        i.remove(force=True)
    return {"action":"DELETE" ,"deleted_containers" :deleted_containers},200

@app.route('/all-containers',methods=['GET'])
def all_containers():
    temp=[]
    for c in client.containers.list(filters={'ancestor':DOCKER_IMAGES}):
        for i in client.df()['Containers']:
            if i['Id'] == c.id:
                break
        temp.append(
            {
                'container_id':c.id,
                'container_name':c.name,
                'container_ports': i['Ports'],
                'container_image': i['Image'],
                'container_state': c.status
            }
        )
    return {"Containers":temp},200



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)

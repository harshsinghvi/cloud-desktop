import docker

from flask import Flask, request, jsonify, render_template, session, redirect
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo,ObjectId

from pytz import timezone
from datetime import datetime

from settings import *

class Username_error(Exception):
    pass 

# Flask app config
app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = FLASK_SECRET_KEY

# database config
app.config['MONGO_URI'] = MONGODB_URI
mongo = PyMongo(app)

#CORS config
CORS(app, support_credentials=True)

# DOCKER CONFIG 
client = docker.from_env() ## for local docker host 
# client = docker.DockerClient(base_url=DOCKER_REMOTE_HOST) ## for remote docker host

# Session Properties
SESSION_DETAILS=['username','authenticated']
USERNAME = SESSION_DETAILS[0]
AUTHENTICATED = SESSION_DETAILS[1]
PASSWORD = 'password'

# TZ
IST = timezone(TIME_ZONE) 

# custom functions
def auth_check(username, password):
    creds = mongo.db.users.find_one({"username":username},{ "_id": 0, "username": 1, "password": 1 })
    if creds['username'] == username and creds['password'] == password:
        return True
    else: 
        return False

# routes 

@app.route('/', methods=['GET', 'POST'])
def root():
    return redirect(FRONTEND_URL)

@app.route('/retry', methods=['GET', 'POST'])
def retry():
    return redirect(FRONTEND_URL+"/retry.html")

@cross_origin()
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return redirect(FRONTEND_URL)
    if AUTHENTICATED in session: 
        logout()
    try:
        username = request.form['username']
        password = request.form['password']
    except:
        return redirect(FRONTEND_URL+"/retry.html")

    if auth_check(username , password ):
        session['username']=username
        session['authenticated']='1'
        return redirect(FRONTEND_URL+"/portal.html")
    return redirect(FRONTEND_URL+"/retry.html")

@cross_origin()
@app.route('/logout', methods = ['POST', 'GET'])
def logout():
    if AUTHENTICATED in session:
        for d in SESSION_DETAILS:
            session.pop(d, None)
    return redirect(FRONTEND_URL)

@cross_origin()
@app.route('/auth', methods = ['POST', 'GET'])
def auth():
    if 'username' in request.args and 'password' in request.args:
        if auth_check(request.form['username'], request.form['password']):
            session['username']=request.args['username']
            session['authenticated']='1'
            return "Auth OK", 200
        else: 
            return "Auth Failed check username and password", 401
    return "No Username or Password supplied in query parms.", 400

@cross_origin()
@app.route('/reset-auth', methods = ['POST', 'GET'])
def reset_auth():
    if AUTHENTICATED in session:
        for d in SESSION_DETAILS:
            session.pop(d, None)
        return "Rest auth Susccefull", 200
    return "Unauthenticated or Unknown Error", 400

@app.route('/test-auth',methods=['GET'])
def test_auth():
    if AUTHENTICATED in session:
        cred = mongo.db.users.find_one({"username":session['username']},{ "_id": 0, "username": 1})
        print(session)
        return "<h1> Authenticated as "+ cred['username'], 200
    return "<h1> Suck it!!  not Authenticated "

@app.route('/service-status', methods = ['GET'])
def service_status():
    return "OK", 200

@cross_origin()
@app.route('/get-data', methods = ['GET'])
def get_data():
    data = {}
    if AUTHENTICATED not in session: 
        data['authenticated'] = 0
        data['msg'] = 'no auth found'
        return data,401
    try:
        username = session['username']
        creds = mongo.db.users.find_one({"username":session["username"]})
        if username != creds['username'] : 
            raise Username_error
    except:
        data['authenticated'] = 0
        data['msg'] = "Auth error or DB Error"
        return data,401
    data['authenticated'] = 1
    data['msg'] = "OK"
    creds.pop("_id")
    creds.pop("password")
    data['data'] = creds
    data['images'] = DOCKER_IMAGES
    return data, 200

@cross_origin()
@app.route('/get-desklet', methods = ['POST']) # add check name too 
def get_desklet():
    return "OK",200
    # return_data = {}
    # if AUTHENTICATED not in session: 
    #     return_data['authenticated'] = 0
    #     return_data['msg'] = 'no auth found'
    #     return return_data,401

    # try:
    #     data = request.get_json()
    # except: 
    #     return "Bad Request",404
    # print(data)
    # return_data = data
    # return return_data, 200
# @app.route('/delete', methods = ['POST', 'GET'])

@app.after_request
def creds(response):
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


@app.route('/pull-images',methods=['GET'])
def pull_images():
    temp=[]
    for image in DOCKER_IMAGES:
        try:
            temp.append(str(client.images.pull(image)))
        except docker.errors.ImageNotFound:
            temp.append(image+" : notfound")
    return {"images":temp}


@app.route('/new-desklet',methods=['GET'])
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


@app.route('/info',methods=['GET'])
def info():
    return client.info()

@app.route('/df',methods=['GET'])
def df():
    return client.df()
    
@app.route('/hello-world',methods=['GET'])
def hello_world():
    return client.containers.run("hello-world", remove=True)

@app.route('/version',methods=['GET'])
def docker_version():
    return client.version()


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)

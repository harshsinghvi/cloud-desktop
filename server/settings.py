from os import path,getenv,urandom
from dotenv import load_dotenv

if path.isfile(".env"):
    load_dotenv(verbose=True)

MONGODB_URI = getenv("MONGO_DB_URI")
DOCKER_REMOTE_HOST=getenv("DOCKER_REMOTE_HOST")

DOCKER_IMAGES=["code:v1", "dorowu/ubuntu-desktop-lxde-vnc"]

DEFAULT_DOCKER_IMAGE=DOCKER_IMAGES[0]

TIME_ZONE = 'Asia/Kolkata'

# FRONTEND_URL='https://cloud-desktop.harshsinghvi.com'
FRONTEND_URL='http://localhost:8000'

FLASK_SECRET_KEY = urandom(12) 
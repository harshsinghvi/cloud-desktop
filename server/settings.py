from os import path,getenv
from dotenv import load_dotenv

if path.isfile(".env"):
    load_dotenv(verbose=True)

MONGODB_URI = getenv("MONGO_DB_URI")
DOCKER_REMOTE_HOST=getenv("DOCKER_REMOTE_HOST")

DOCKER_IMAGES=["code:v1"]

DEFAULT_DOCKER_IMAGE=DOCKER_IMAGES[0]
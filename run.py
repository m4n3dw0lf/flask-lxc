
from flask import Flask
from app import container as container_api

if __name__ == "__main__":
   app = Flask(__name__)
   app.register_blueprint(container_api)
   app.run(host="0.0.0.0",threaded=True)


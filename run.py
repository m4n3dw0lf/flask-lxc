
from flask import Flask
from flask_lxc import lxc_api

if __name__ == "__main__":
   app = Flask(__name__)
   app.register_blueprint(lxc_api)
   app.run(host="0.0.0.0",threaded=True)


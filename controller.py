from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask, jsonify, request
import math
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def main_api():
    return jsonify({"message":"You are in flask-mysql-api"})



if __name__=="__main__":
    app.run(threaded=True,host="0.0.0.0")
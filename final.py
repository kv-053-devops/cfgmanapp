import sys
from flask import Flask, request, jsonify, make_response, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from google.cloud import storage
import json
import random


# Init app flask
app = Flask(__name__)

user = os.environ.get('USER_DB', 'postgres')
pw = os.environ.get('PW', 'postgres')
db = os.environ.get('DB', 'postgres')
host_db = os.environ.get('HOST_DB', 'localhost')
port = os.environ.get('PORT_DB', '5432')
   
POSTGRES = {
    'user': user,
    'pw': pw,
    'db': db,
    'host': host_db,
    'port': port,
}


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)
#key = ["ozJJnnNAuL6d7f80upQobuq04lRjB0Mc4DqseClvEgONmPz6bxTSN3GkG9qP","dFwKiqcvZnE7Y6lDy6rBxnwkXZFo4UrP6iyKCWJ5ENOzT0zy3uVhboFAIXcN",
    #       "fV511EA1BuSOvQz9dvwOaggCC8jVtHUSyileRc58artpzNsU5OjLSIoIMkMT", "bQgHpBb0Ro9qJdc3uI92AkhbgKQmkheQwFc2HogQ5XgkCThGCCacRyLPGAZv",
     #      "Qrryp9yY35JyX8Fn93QQKiONuEJnPnAWHuH956GZsBCLhsbcOotRCgP2fSAN", "Ok83lRmuDMCP3LhCtUOdMaA5K6eRF3BAdCYWrg4kEva8Lh0GkdwEAOcQqenJ"]

class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    interval = db.Column(db.Integer)
    range = db.Column(db.Integer)
    name = db.Column(db.String(255))
    symbol = db.Column(db.String(100))
    

# Data Schema
class DataSchema(ma.Schema):
    class Meta:
        fields = ('id', 'interval', 'range', 'name', 'symbol')

products_schema = DataSchema(many=True)

# Create up
@app.route('/save', methods=['PUT'])
def up_data():
    try:
        if request.method == 'PUT':
            loaded = request.get_json()
            symbol = loaded['symbol']
            d = Data.query.all()
            d[0].symbol = symbol
            db.session.commit()

    except:
         print("Problem with method 'PUT'")

    return make_response("", 200)


# Get All
@app.route('/start', methods=['GET'])
def get_all():
    d = Data.query.all()
    result = d[0].symbol
    return jsonify(result.data)



####################################
#taking JSON with templates from GCS

FILE_REAL_TIME = 'real_time.json'
FILE_INTRADAY = 'intraday.json'


########################
#Making endpoints of API for access from other microservices
@app.route('/conf/query', methods=['GET'])
def request_take():
    #token = random.randint(0, 5);
    if request.method == 'GET':
        query_type = request.args.get('query_type')
        if query_type == "realtime":
            results = {"remote_api_url": "https://api.worldtradingdata.com",
                       "query_template": "/api/v1/stock?",
                       "remote_api_token": "ozJJnnNAuL6d7f80upQobuq04lRjB0Mc4DqseClvEgONmPz6bxTSN3GkG9qP"}

            return jsonify(results)

        elif query_type == "intraday":
            results = {"remote_api_url": "https://intraday.worldtradingdata.com",
                       "query_template": "/api/v1/intraday?",
                       "remote_api_token": "ozJJnnNAuL6d7f80upQobuq04lRjB0Mc4DqseClvEgONmPz6bxTSN3GkG9qP"}
            return jsonify(results)
    else:
        return "UNKNOWN QUERY TYPE"


if __name__ == '__main__':
    d = Data( interval =2, range=2, name="Microsoft,Amazon,Apple,Alphabet,Facebook", symbol="MSFT,AMZN,AAPL,GOOGL,FB")
    db.create_all()
    db.session.add(d)
    db.session.commit()

    app.debug = True
    app.run(host='0.0.0.0', port =5004)

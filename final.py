import sys
from flask import Flask, request, jsonify, make_response, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from google.cloud import storage
import json


# Init app
app = Flask(__name__)

if len(sys.argv) != 1 :
    host_db = sys.argv[1]
else:
    host_db = 'localhost'
POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'name',
    'host': host_db,
    'port': '5432',
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

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
    all = Data.query.all()
    result = products_schema.dump(all)
    return jsonify(result.data)



####################################
#taking JSON with templates from GCS

FILE_REAL_TIME = 'real_time.json'
FILE_INTRADAY = 'intraday.json'


########################
#Making endpoints of API
@app.route('/conf/query', methods=['GET'])
def request_take():
    if request.method == 'GET':
        query_type = request.args.get('query_type')
        if query_type == "realtime":
            results = {"remote_api_url" : "https://api.worldtradingdata.com",
                        "query_template" : "/api/v1/stock?",
                        "remote_api_token" : "Ok83lRmuDMCP3LhCtUOdMaA5K6eRF3BAdCYWrg4kEva8Lh0GkdwEAOcQqenJ"}

            return jsonify(results)

        elif query_type == "intraday":
            results = {"remote_api_url" : "https://intraday.worldtradingdata.com",
                        "query_template" : "/api/v1/intraday?",
                        "remote_api_token" : "Ok83lRmuDMCP3LhCtUOdMaA5K6eRF3BAdCYWrg4kEva8Lh0GkdwEAOcQqenJ"}
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

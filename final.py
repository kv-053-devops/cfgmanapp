from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os
import json
from google.cloud import storage
from google.oauth2 import service_account


import json
import os

# Init app
app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'name',
    'host': 'localhost',
    'port': '5432',
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://name:qwerty@localhost:5432/postgres'


#basedir = os.path.abspath(os.path.dirname(__file__))
# Database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    interval = db.Column(db.Integer) #2
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
        # loaded = json.loads(file)
            symbol = loaded['symbol']
            d = Data.query.all()
            d[0].symbol = symbol

        #range = loaded['range']
        #interval = loaded['interval']
        #d = Data.query.all()
        #d[0].interval = interval
        #d[0].range = range

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
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gcs.json'
storage_client = storage.Client()
STORAGE_BUCKET = '237659812347654kjkjhjhgj68665'
FILE_REAL_TIME = 'real_time.json'
FILE_INTRADAY = 'intraday.json'

########################
#Making endpoints of API
@app.route('/conf/query', methods=['GET'])
def request_take():
    if request.method == 'GET':
        query_type = request.args.get('query_type')
        if query_type == "realtime":
            client = storage.Client()
            bucket = client.get_bucket(STORAGE_BUCKET)
            blob = bucket.get_blob(FILE_REAL_TIME)
            json_data = blob.download_as_string()
            return json.loads(json_data.decode('UTF-8'))

        elif query_type == "intraday":
            client = storage.Client()
            bucket = client.get_bucket(STORAGE_BUCKET)
            blob = bucket.get_blob(FILE_INTRADAY)
            json_data = blob.download_as_string()
            return json.loads(json_data.decode('UTF-8'))
    else:
        return "UNKNOWN QUERY TYPE"


if __name__ == '__main__':
    d = Data( interval =2, range=2, name="Microsoft,Amazon,Apple,Alphabet,Facebook", symbol="MSFT,AMZN,AAPL,GOOGL,FB")
    db.create_all()
    db.session.add(d)
    db.session.commit()

#    app.debug = True
    app.run(port =5004)

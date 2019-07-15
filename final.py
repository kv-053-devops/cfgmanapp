from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
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
    interval = db.Column(db.Integer)
    range = db.Column(db.Integer)
    name = db.Column(db.String(255))
    sumbol = db.Column(db.String(100))
    # record_to_insert = ('range', 1)
    # record_to_insert = ('interval', 2)
    # record_to_insert = ('name', "Microsoft,Amazon,Apple,Alphabet,Facebook")
    # record_to_insert = ('sumbol', "MSFT,AMZN,AAPL,GOOGL,FB")


# Data Schema
class DataSchema(ma.Schema):
    class Meta:
        fields = ('id', 'interval', 'range', 'name', 'sumbol')

products_schema = DataSchema(many=True)

# Create up
@app.route('/save', methods=['PUT'])
def up_data():
    # try:
    if request.method == 'PUT':
        loaded = request.get_json()
        # loaded = json.loads(file)
        sumbol = loaded['symbol']
        d[0].sumbol = sumbol

        #range = loaded['range']
        #interval = loaded['interval']
        #d = Data.query.all()
        #d[0].interval = interval
        #d[0].range = range

        db.session.commit()

    # except:
    #     print("This didn't work.")

    return make_response("", 200)


# Get All
@app.route('/start', methods=['GET'])
def get_all():
    all = Data.query.all()
    result = products_schema.dump(all)
    return jsonify(result.data)

if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run()
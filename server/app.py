#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

# - GET /bakeries: returns a list of JSON objects for all bakeries in the database.
# - GET /bakeries/<int:id>: returns a single bakery as JSON with its baked goods nested in a list.
#   Use the id from the URL to look up the correct bakery.
# - GET /baked_goods/by_price: returns a list of baked goods as JSON, sorted by price in descending order.
#   (HINT: how can you use SQLAlchemy to sort the baked goods in descending order?)
# - GET /baked_goods/most_expensive: returns the single most expensive baked good as JSON.
#   (HINT: how can you use SQLAlchemy to sort the baked goods in descending order and limit the number of results?)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    response = make_response(
        bakeries,
        200
    )
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery_dict = bakery.to_dict()
    response = make_response(
        bakery_dict,
        200
    )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    # .desc() is what orders it in descending order
    #baked_goods_dict = baked_goods.to_dict()
    baked_goods_list = [bg.to_dict() for bg in baked_goods]
    response = make_response(
        baked_goods_list,200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    # .limit(1) makes sure we only return the first result from our list, which would be the most expensive
    baked_goods_dict = baked_goods.to_dict()
    response = make_response(
        baked_goods_dict, 200
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)

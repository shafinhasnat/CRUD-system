from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_cors import CORS, cross_origin
from functools import wraps
import jwt


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/*": {"origins": "*"} })

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'mieisthebestmiedaytekhubmojahobe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  description = db.Column(db.String(200))
  price = db.Column(db.Float)
  qty = db.Column(db.Integer)

  def __init__(self, name, description, price, qty):
    self.name = name
    self.description = description
    self.price = price
    self.qty = qty
  def __repr__(self):
    return f"Product('{self.id}', '{self.name}', '{self.price}', '{self.qty}')"

class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description', 'price', 'qty')

# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)



def token():
  encoded_jwt = jwt.encode({'admin': 'shafinhasnat'}, app.config['SECRET_KEY'])
  return encoded_jwt.decode('UTF-8')
# print(token())
# print(jwt.decode(token(), app.config['SECRET_KEY']))

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = request.args.get('token')
    if not token:
      return jsonify({'message': 'the token is missing'})
    try:
      data = jwt.decode(token, app.config['SECRET_KEY'])
    except:
      return jsonify({'message': 'the token is invalid'})
    return f(*args, **kwargs)
  return decorated

@app.route('/protected')
@token_required
def protected():
  return jsonify({'message': 'valid access'})


@app.route('/product', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
@token_required
def product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']
    new_product = Product(name=name, description=description, price=price, qty=qty)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

@app.route('/',methods=['GET'])
@token_required
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def home():
  all_products = Product.query.all()
  result = products_schema.dump(all_products)
  return jsonify(result)

@app.route('/product/id/<id>', methods=['GET'])
@token_required
def get_product(id):
  product = Product.query.get(id)
  result = product_schema.dump(product)
  print(result)
  return jsonify(result)

@app.route('/product/name/<name>')
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
@token_required
def get_product_name(name):
  product = Product.query.filter_by(name=name).all()
  result = products_schema.dump(product)
  return jsonify(result)

@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
  product = Product.query.get(id)
  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']
  product.name = name
  product.description = description
  product.price = price
  product.qty = qty
  db.session.commit()
  return product_schema.jsonify(product)

@app.route('/product/<id>', methods=['DELETE'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
@token_required
def delete_product(id):
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()
  return product_schema.jsonify(product)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
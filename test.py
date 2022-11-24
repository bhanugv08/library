from flask_mongoengine import MongoEngine
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt

import datetime
import hashlib


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "host":"localhost",
    "port":,
    "db": "Digilib"
}
db = MongoEngine(app)

jwt = JWTManager(app) # initialize JWTManager

app.config['JWT_SECRET_KEY'] = 'Digilib_Secret_Key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1) # define the life span of the token

class User(db.Document):
    name = db.StringField(required=True)
    email = db.EmailField(required=True)
    password = db.StringField(required=True)
    mobile = db.IntField(required=True, min_value=6000000000, max_value=9999999999)
    isAdmin = db.IntField(required=True) # 0 is user

@app.route("/user/",methods=["POST"])
def create_user():
    new_user = request.get_json()
    new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest()  # encrpt password
    user_from_db = User.objects(email=new_user['email']).first()
    if not user_from_db:
        user = User(**new_user).save()
        return jsonify(user), 201
    else:
        return jsonify({'msg': 'Username already exists'}), 409

@app.route("/login", methods=["POST"])
def login():
    login_details = request.get_json() # store the json body request
    user_from_db = User.objects(email=login_details['email']).first()
    if user_from_db:
        encrpted_password = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
        if encrpted_password == user_from_db['password']:
            additional_claims = {"role": "user" if user_from_db['isAdmin'] == 0 else "admin"}
            access_token = create_access_token(identity=user_from_db['email'], additional_claims=additional_claims) # create jwt token
            return jsonify(access_token=access_token), 200
    return jsonify({'msg': 'The username or password is incorrect'}), 401

@app.route("/user")
@jwt_required()
def profile():
    current_user = get_jwt_identity() # Get the identity of the current user
    user_from_db = User.objects(email=current_user).first()
    if user_from_db:
        return jsonify({'profile' : user_from_db }), 200
    else:
        return jsonify({'msg': 'Profile not found'}), 404

class Book(db.Document):

    title = db.StringField(required=True)
    author = db.StringField(required=True)
    bookId = db.IntField(required=True)

@app.route('/books')
@jwt_required()
def get_book_list():
    books = Book.objects()
    return jsonify(books, 200)

@app.route('/books/', methods=["POST"])
@jwt_required()
def add_book():
    claims = get_jwt()
    if (claims["role"] != "admin"):
        return jsonify({'msg': 'User not authorized to create books'}), 401
    new_book = request.get_json()
    book = Book(**new_book).save()
    return jsonify(book), 201


@app.route('/books/<id>')
@jwt_required()
def getBook(id: str):
    book = Book.objects.first_or_404(id=id)
    return book.to_dict(), 200

@app.route('/books/<id>', methods=['PUT'])
@jwt_required()
def update_book(id):
    json_data = request.get_json()
    book = Book.objects.get_or_404(id=id)
    book.update(**json_data)
    return jsonify(str(book.id)), 200

@app.route('/books/<id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    book = Book.objects.get_or_404(id=id)
    book.delete()
    return jsonify(str(book.id)), 200

if __name__=='__main__':
    app.run()
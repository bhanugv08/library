from flask_mongoengine import MongoEngine
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "host":"localhost",
    "port":27017,
    "db": "Mylib"
}
db = MongoEngine(app)

class User(db.Document):
    name = db.StringField(required=True)
    email = db.EmailField(required=True)
    password = db.StringField(required=True)
    mobile = db.IntField(required=True, min_value=6000000000, max_value=9999999999)
    isAdmin = db.IntField(required=True) # 0 is user

class Book(db.Document):
	title = db.StringField(required=True)
	author = db.StringField(required=True)
	bookId = db.IntField(required=True)


@app.route('/book/', methods=["POST"])
def add_book():
    new_book = request.get_json()
    book = Book(**new_book).save()
    return jsonify(book), 201

@app.route("/user/",methods=["POST"])
def create_user():
	new_user = request.get_json()
	user = User(**new_user).save()
	return jsonify(user), 201

if __name__=='__main__':
    app.run()
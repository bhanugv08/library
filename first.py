from flask import Flask,make_response,jsonify,Response,request
from flask_mongoengine import MongoEngine
import mongoengine as me
import json
import pymongo


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "host":"localhost",
    "port":27017,
    "db": "Digilib"
}
db = MongoEngine(app)


@app.route("/users",methods=["POST"])
def create_user():
    try:
        json_data = request.json
        dbResponse = db.users.insert_one(json_data)
        print(dbResponse.inserted_id)
        return Response(
            response=json.dumps(
                {
                    "message":"user created",
                    "id":f"{dbResponse.inserted_id}",
                }
            ),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
"""class Library(db.Document):
    book_id=db.IntField()
    name=db.StringField(required=True)
    author=db.StringField()

    def to_json(self):
        return {
            "book_id":self.book_id,
            "name":self.name,
            "author":self.author
        }

@app.route('/booklist',methods=['POST'])
def booklist():
     # book1=Library(book_id=1,name="python",author="JF.BIERD")
     # book2=Library(book_id=2,name="JAVA",author="REIN MARTIN")
     # book1.save()
     # book2.save()
     return Response("",201)
"""
# class Book(me.Document):
#     title = me.StringField(required=True)
#     id = me.IntField()
#     year = me.IntField()
#     rated = me.StringField()
#     authors = me.ListField()

# bttf = Book(title="Back To The Future", year=1985)
# bttf.actors = [
#     "Michael J. Fox",
#     "Christopher Lloyd"
# ]
# bttf.save()

if __name__=='__main__':
    app.run()
from flask import Flask,Response,request
#from user import routes
import pymongo
import json



app=Flask(__name__)
#database
try:
    mongo=pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.Digilib
    mongo.server_info()
except:
    print("ERROR-Cannot connect to db")
#db=client.user_login_system

#from user import routes

@app.route("/users",methods=["POST"])
def create_user():
    try:
        json_data = request.json

        # user={
        #     "name":"BHANU",
        #     "EMAIL":"bhanu.gv08@gmail.com",
        #     "location":"Bangalore"
        # }
        dbResponse = db.users.insert_one(json_data)
        print(dbResponse.inserted_id)

        return Response(
            response=json.dumps(
                {"message":"user created",
                 "id":f"{dbResponse.inserted_id}",
                 }

            ),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)

class Library(db.document):
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
    book1=Library(book_id=1,name="python",author="JF.BIERD")
    # book2=Library(book_id=2,name="JAVA",author="REIN MARTIN")
    book1.save()
    # book2.save()
    return Response("PYCHARM",201)






if __name__=='__main__':
    app.run()
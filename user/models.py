from flask import Flask,jsonify,request
from app import db


class user:

    def signup(self):
        print(request.form)

        user={

            "name":request.form.get('name'),
            "email":request.form.get('email'),
            "password":request.form.get('password')
        }

        if db.users.find_one({"email":user['email']}):
            return jsonify({"error":"Email address already in use"}),400

        if db.users.insert_one(user):
            return jsonify(user),200

        return jsonify({"error":"signup failed"}),400

class Library:
    def book(self):
        book={
            "name"
        }

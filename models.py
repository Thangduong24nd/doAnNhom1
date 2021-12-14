import datetime
from app import db
from flask import Flask, render_template, request,redirect,flash,url_for
from app import login 
from werkzeug.security import generate_password_hash,check_password_hash
from geoalchemy2 import Geometry
from flask_login import UserMixin
class places(db.Model):
   __tablename__="places"
   id =db.Column(db.Integer, primary_key=True)
   geom=db.Column(Geometry('POINT'))
   address=db.Column(db.String, nullable=True)
   phoneNum=db.Column(db.String, nullable=True)
   name=db.Column(db.String, nullable=True)
   numVote=db.Column(db.Integer, nullable=True)
   rate=db.Column(db.Integer, nullable=True)
   openH=db.Column(db.Integer, nullable=True)
   closeH=db.Column(db.Integer, nullable=True)
   type=db.Column(db.Integer, nullable=True)
   Comment =db.relationship("Comments")


class Users(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user= db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String)
    Comments =db.relationship("Comments")
    def set_password(self, passwordInput):
        self.password = generate_password_hash(passwordInput)

    def check_password(self, passwordInput):
        return check_password_hash(self.password, passwordInput)


class Comments(db.Model):
   __tablename__="comments"
   id = db.Column(db.Integer, primary_key=True)
   reply_id =db.Column(db.Integer, nullable=True,default=0)
   user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
   places_id = db.Column(db.Integer, db.ForeignKey("places.id"), nullable=False)
   texts =db.Column(db.String)
   imgs =db.Column(db.String)
   def reply(self,texts,imgs,user_id):
      rep = Comments(reply_id=self.id,user_id=user_id,texts=texts,imgs=imgs,places_id=self.places_id)
      return rep


@login.user_loader
def load_user(id):
   return Users.query.get(int(id))
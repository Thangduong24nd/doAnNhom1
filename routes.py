from typing import Text
from app import app
from app.models import *
from app.form import *
from flask import Flask, render_template, request,redirect,flash,url_for
from sqlalchemy.sql.functions import current_user
from flask_login.utils import *
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import or_ , and_,func
from flask.helpers import flash, url_for
from datetime import *
from datetime import date
from flask.json import jsonify
import json

@app.route("/getdata1")
def getdata1():
    return render_template("test2.html") 
@app.route("/getdata", methods=['POST','GET'])
def getdata():
    lats = request.form.getlist("lats")
    lngs = request.form.getlist("lngs")
    names = request.form.getlist("names")
    phones = request.form.getlist("phones")
    addrs = request.form.getlist("addrs")
    for i in range(0,len(lats)) :
        lng=lngs[i]
        lat=lats[i]
        addr=addrs[i]
        phone=phones[i]
        name=names[i]
        geom=func.ST_GeomFromText(f'POINT({lng} {lat})',4326)
        place = places(name=name,address=addr,phoneNum=phone,numVote=0,rate=0,openH=7,closeH=23,geom=geom)
        db.session.add(place)
        db.session.commit()
        
    return render_template('a.html')
@app.route("/api")
def postGIS_api2():
    apis = db.session.query( places.id,places.name,places.phoneNum,places.address, places.numVote,places.rate,places.openH,places.closeH,\
    func.ST_AsGeoJSON(func.ST_Transform(places.geom,4326)).label('geometry')).all()
    rs =[]
    for api in apis:
        properties_temp={
            "id": api.id,
            "name": api.name,
            "phoneNum":api.phoneNum,
            "numVote": api.numVote,
            "address":api.address,
            "rate":api.rate,
            "openH" :api.openH,
            "closeH" : api.closeH
        }
        geometry_temp = json.loads(api.geometry)
        
        feature = {
            "type": "Feature",
            "properties": properties_temp,
            "geometry": geometry_temp
        }
        rs.append(feature)
    return jsonify({
                #"type":"FeatureCollection",
                "features": rs
 
        })
@app.route("/index")
def  index():
    return render_template("index.html")
@app.route("/crud")
def crud():
    return render_template("crud.html")
@app.route("/add", methods=["GET","POST"])
def add():
    # id= request.args.get('id')
    name= request.args.get('name')
    address= request.args.get('address')
    phoneNum= request.args.get('phoneNum')
    numVote= request.args.get('numVote')
    rate= request.args.get('rate')
    openH= request.args.get('openH')
    closeH= request.args.get('closeH')
    lat=request.args.get('lat')
    lng=request.args.get('lng')
    geom=func.ST_GeomFromText(f'POINT({lng} {lat})',4326)
    new = places(name=name,address=address,phoneNum=phoneNum,numVote=numVote,rate=rate,openH=openH,closeH=closeH,geom=geom)
    db.session.add(new)
    db.session.commit()
    return render_template('ok.html')
@app.route("/delete", methods=["GET","POST"])
def delete():
    id=request.args.get('id')   
    delete = places.query.get(id)
    db.session.delete(delete)
    db.session.commit()
    return render_template('ok.html')
@app.route("/update",methods=["GET","POST"])
def update():
    id=request.args.get('id1')  
    name=request.args.get('name')
    address=request.args.get('address')
    phoneNum=request.args.get('phoneNum')
    numVote=request.args.get('numVote')
    rate=request.args.get('rate')
    openH=request.args.get('openH')
    closeH=request.args.get('closeH')
    f=places.query.get(id)
    f.name=name
    f.address=address
    f.phoneNum=phoneNum
    f.numVote=numVote
    f.rate=rate
    f.openH=openH
    f.closeH=closeH
    db.session.commit()
    return render_template('ok.html')



@app.route("/signUp",methods=['POST','GET'])
def signUp():
    form = signUpForm()
    if form.validate_on_submit():
        user = form.user.data
        password = form.password.data
        newUser= Users(user=user,password=password)
        newUser.set_password(form.password.data) 
        db.session.add(newUser)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('signUp'))
    return render_template("signup.html", form=form) 

@app.route("/login",methods=['POST','GET'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user= Users.query.filter_by(user=form.user.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        flash('Đăng nhập thành công')
        return redirect('index')
    return render_template('login.html', form=form)
@app.route("/logout")
def logout():
    logout_user()
    return redirect('login')
@app.route("/comment_s1")
def comment_s1():
    return render_template("addcomment.html")
@app.route("/comment",methods=['GET', 'POST'])
def comment():
    places_id= int(request.form.get('places_id'))
    texts= request.form.get('texts')
    imgs=request.form.get('imgs')
    comment = Comments(user_id=current_user.get_id(),places_id=places_id,texts=texts,imgs=imgs)
    db.session.add(comment)
    db.session.commit()
    return render_template("index.html",title='Index')
@app.route("/reply",methods=['GET', 'POST'])
def reply():
    cmt_id= request.form.get("cmt_id")
    cmt= Comments.query.get(cmt_id)
    texts= request.form.get('texts')
    imgs=request.form.get('imgs')
    db.session.add(cmt.reply(texts,imgs,current_user.get_id()))
    db.session.commit()
    return render_template("index.html",title='Index')
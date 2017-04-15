from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app import app,db,requires_auth,login_manager
from functools import wraps
from flask import render_template,session
from app.user.models import User
from app.forms.models import LoginForm,RegisterForm
from flask import Blueprint, request, render_template,flash, g, session, redirect, url_for, jsonify, make_response
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, DateField, SelectField,IntegerField, SelectMultipleField
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms.validators import InputRequired, Email, Length,URL
import random
random = random.SystemRandom()
mod_user = Blueprint('user', __name__)
''' 
def get_random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
'''
"""
    Returns a securely generated random string.
 
    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits.
 
    Taken from the django.utils.crypto module.
"""
   # return ''.join(random.choice(allowed_chars) for i in range(length))
# because models.py is in this file
# we are not writing app.route instead of it we are writing @mod_user
# blueprint is use to define routes
# prefix is defined for all routes in this file
# we are importing this blueprint object and registering it in __init__.py
'''
@mod_user.route('/login', methods=['GET'])
def check_login():
    if 'user_id' in session:
        user = User.query.filter(User.id == session['user_id']).first()
        return jsonify(success=True, user=user.to_dict())

    return jsonify(success=False), 401
'''
@app.before_request
def blueprintefore_request():
    g.user = current_user
'''
@mod_user.before_request
def fun():
    #session.pop('csrf_key')
    if request.method == 'GET':
        print(session)
        session.clear()
        print('generatecsrf_key')
        print('after every request key cahnges')
        if 'csrf_key' not in session or session['csrf_key'] == 'n':
            print('random string')
            session['csrf_key'] = get_random_string()
        print(session['csrf_key'])
        app.jinja_env.globals['csrf_key'] = session['csrf_key']
        print(session)
        print(app.jinja_env.globals['csrf_key'])
    
@mod_user.before_request
def csrf_protect():
    if request.method == "POST":
        print(session)
        #print(app.jinja_env.globals['csrf_key'])
        token = session['csrf_key']
        session['csrf_key']= 'n'
        print(session)
        print(token)
        print(type(token))
        print(token == 'n')
        print(request.form.get('csrf_key'))
        if token == 'n' or token != app.jinja_env.globals['csrf_key']:#request.form.get('csrf_key'):
            print(render_template)
            print('yo')
            print('hello')
            print('sdkshdjshksdhkdshs')
            return render_template('401.html')   
            print('after return')       
'''    


@mod_user.route('/login', methods=['GET', 'POST'])
def login():
    print("/login")
    if not session.get('k'):
        session['k'] = "http://127.0.0.1:5000/home"
    if 'user_id' in session:
        return redirect(session['k'])
    print("dscksjck")
    print(session['k'])
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            print(user.password)
            print(form.password.data)
            if check_password_hash(user.password, form.password.data):
                session['user_id'] = user.id
                p =  session['k']
                login_user(user)
                session['k'] = p

                print(session['k'])
                return redirect(session['k'])
            return render_template('login.html', form=form,message= "password is incorrect")
        else:
            return render_template('login.html', form=form,message= "Email is not registered")
    return render_template('login.html', form=form)

@mod_user.route('/logout')
def logout():
    g.user = None
    session.clear()
    logout_user()
    ans = {'log':"Login",'val':"Signup"}
    return redirect("http://127.0.0.1:5000/home")
'''
@mod_user.route('/register', methods=['GET','POST'])
def signup():
    if 'user_id' in session:
        return redirect("http://127.0.0.1:5000/home")
    print('nothing ran')        
    form = RegisterForm()
    print('/register')
    if form.validate_on_submit():
        if form.password.data != form.check_password.data:
            return render_template('register.html', form=form ,message = "Passwords don't match")
        if '@' not in form.email.data:
            return render_template('register.html',form=form, message="Please enter a valid email")
        try:
            print('user added')
            new_user = User(name=form.username.data, email=form.email.data, password=form.password.data,is_admin=False)
            db.session.add(new_user)
            db.session.commit()
            app.jinja_env.globals['csrf_key'] = get_random_string()
            session.clear()
            print('user added')
            #print('lalala')
            #print(new_user.id)
            session.clear()
            print(session)
            #session.pop('user_id')
            #print(session)
            #for key in session.keys():
            #   session.pop[key]
            #print(session)


            #session['user_id'] = new_user.id
            print(new_user.id)
            #print(session['user_id'])
            login_user(new_user)
            #print(session['user_id'])
            #print(session['csrf_key'])
            #print(session)
            return redirect("http://127.0.0.1:5000/home")
        except:
            print('user not added')
            return render_template('register.html', form=form, message = "Email is already Registered")
    return render_template('register.html', form=form)
'''
#This route is needed to show user's booking history
@mod_user.route('/api/user_info', methods=['GET'])
def get_user_info():
    try:
        if 'user_id' in session:
            user_id = session['user_id']
        else:
            print('notloggedin')
            return jsonify(success=False), 404
        user_touple = User.query.filter(User.id == user_id).first()
        name = user_touple.name
        email = user_touple.email
        id = user_touple.id
        return jsonify(success=True, info={'name':name, 'email':email,'id':id})
    except:
        return jsonify(success=False, message="Error in fetching user info"), 404

from flask import render_template, request, flash, session, url_for, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from app import app, login_manager
import sqlite3
import logging
import config as CONFIG

class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password
        self.authenticated = False
         
    def is_active(self):
        return self.is_active()

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def get_id(self):
        return self.id


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')
    
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    #print("load_user:")
    conn = sqlite3.connect(CONFIG.DATABASE)
    curs = conn.cursor()
    query = """SELECT * from "users" where "id" = "{0}";""".format(userid)
    #print("query:", query)
    curs.execute(query)
    row = curs.fetchone()  #return class tuple
    #print("returned row", row)
    #print(type(row))
    if row is None:
        #print("user not found:")   
        return None
    else:
        #print("user found:")
        #print("row0:",row[0])
        return User(row[0], row[1], row[2])
    

@app.route("/login", methods=['GET','POST'])
def login():
    #logging.info("login()")
    form = LoginForm()
    if request.method == "GET":
        #logging.info("GET")
        #query_string = request.query_string
        username = request.args.get('username')
        #logging.info("username:")      
        #logging.info(username)
        password = request.args.get('password')
        #logging.info("password:")      
        #logging.info(password)
        #logging.info("querystring:")
        #logging.info(query_string)
        if username != None:
            if (len(username) != 0) and (len(password) != 0):
                #logging.info("login()[inside]")
                conn = sqlite3.connect(CONFIG.DATABASE)
                cursor = conn.cursor()
                select = cursor.execute("""SELECT * FROM "users" where "username" = "{0}";""".format(username))
                try:
                    row = list(cursor.fetchone())
                    logging.info(row)
                    if (username == row[1]) and (password == row[2]):
                        id = row[0]
                        user = User(id,username,password)
                        current_user.authenticated = True
                        # print("x:", current_user.authenticated)
                        login_user(user)
                        cursor.close()
                        conn.close() 
                        return redirect('/')
                    else: 
                        return redirect('/')                    
                except Exception as e:
                    logging.info("exception at login (ERR:1234):")
                    cursor.close()
                    conn.close() 
                    return redirect('/')
        else:
             return render_template('login.html',title='Login', form=form) 
 

@app.route('/logout', methods=['GET','POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect('/')
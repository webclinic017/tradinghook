from flask import render_template, request, flash, session, url_for, redirect
from flask_login import logout_user, login_required, current_user
from app import app
#from app import tradecode as *
from app.tradecode import *

# --------------------------------------------------------

    
@app.route('/', methods=['GET'])
def root():
  if current_user.is_authenticated:
     return render_template("home.html")
  return render_template("login.html")


@app.route('/logout')
@login_required
def route_logout():
    logout_user()
    if session.get('was_once_logged_in'):
        # prevent flashing automatically logged out message
        del session['was_once_logged_in']
    flash('You have successfully logged yourself out.')
    return redirect('/')


@app.route("/webhook", methods=['GET','POST'])
def webhook():
  data = request.data
  if data != b'':
    parse(data)
  return("Thanks!")

  
@app.route('/account', methods=['GET'])
def account():
  account = query_accountbalance(1)
  balance = f"{account.settled + account.unsettled:.2f}"
  settled = f"{account.settled:.2f}"
  unsettled = f"{account.unsettled:.2f}"
  return render_template("account.html", a=balance, b=settled, c=unsettled)


@app.route('/positions', methods=['GET'])
def positions():
    return render_template("positions.html")


@app.route('/conditions', methods=['GET'])
def conditions():
    return render_template("conditions.html")


@app.route('/capital', methods=['GET'])
def captial():
  return render_template("capital.html")


@app.route('/settings', methods=['GET'])
def general():
  return render_template("settings.html")


@app.route('/home', methods=['GET'])
def home():
  return render_template("home.html")


@app.route('/utility', methods=['GET','POST'])
def utility():
  if request.method == 'POST':
        if request.form['submit_a'] == 'submit_a':
            create_blank_accountbalance()
  return render_template("utility.html")


@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('result.html', result = dict)

   
@app.route('/result2')
def result2():
   rows = return_position("x")
   df = list_to_df(rows)
   return render_template('result2.html', tables=[df.to_html(classes='data')], titles=df.columns.values)   


@app.route('/result3')
def transactions():
   rows = return_transactions()
   df = transactions_to_df(rows)
   return render_template('result3.html', tables=[df.to_html(classes='data')], titles=df.columns.values)  
   
  
@app.errorhandler(404)
def invalid_route(e):
  return render_template("404.html")
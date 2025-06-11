from AppFactory import create_app
from flask import (Flask, redirect, url_for, request,
                   render_template, make_response, session)
from flask_sqlalchemy import SQLAlchemy
import secrets

"""app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.testmtg.db'
db = SQLAlchemy(app)
"""

app = create_app()

@app.route('/student')
def student():
   return render_template('student.html')


@app.route('/cookies/')
def cookies():
    return render_template('cookies.html')

@app.route('/setcookie', methods=['GET', 'POST'])
def setcookie():
    if request.method == 'POST':
        user = request.form['nm']
        resp= make_response(render_template('readcookie.html'))
        resp.set_cookie('userID', user)
        return resp
    else:
        return None

@app.route('/getcookie')
def getcookie():

    name = request.cookies.get('userID')
    return f'<h1>welcome {name}</h1>'

@app.route('/sessions/')
def sessions():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + "<b><a href = '/logoutWithSession'>click here to log out</a></b>"


    return "You are not logged in <br><a href = '/loginWithSession'></b>" + \
        "click here to log in</b></a>"


@app.route('/loginWithSession', methods=['GET', 'POST'])
def login_with_session():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('sessions'))
    return '''

   <form action = "" method = "post">
      <p><input type = \'text\' name = \'username\'/></p>
      <p<<input type = submit value = loginWithSession/></p>
   </form>

   '''

@app.route('/logoutWithSession')
def logout():
    session.pop('username', None)
    return redirect(url_for('sessions'))

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)


@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/greet/<name>')
def greet(name):
    if name == 'Picciotto':
        return redirect(url_for("pet"))
    else:
        return render_template("greet.html", name = name)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('greet', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('greet', name=user))


@app.route('/assess/<string:name>/<int:score>/')
def assess(name, score):
    return render_template('assess.html', marks=score, name=name)

@app.route('/kitty')
def pet():
    return "snuggling youuuu"

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            debug=True)


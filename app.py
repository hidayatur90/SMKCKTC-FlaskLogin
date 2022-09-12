from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = "smk_cinta"
app.config['MONGO_URI'] = "mongodb://localhost:27017/smk_cinta"

mongo = PyMongo(app)

@app.route("/")
def index():
    if 'username' in session:
        this_session = session['username']
        return render_template('login.html', session_user = this_session)
    return render_template('index.html')

@app.route("/login", methods=['POST'])
def login():

    users = mongo.db.users
    login_user = users.find_one({
        "name": request.form['username']
    })

    if login_user:
        pw_hash = bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'])
        if pw_hash == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Username atau password salah!'

@app.route("/register", methods=['POST', 'GET'])
def register():

    if request.method == "POST":
        users = mongo.db.users
        user_exist = users.find_one({
            "name": request.form['username']
        })

        if user_exist is None:
            pw_hash = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({
                "name": request.form['username'],
                "password" : pw_hash
            })
            return redirect(url_for("index"))

        return "Username telah digunakan!"

    return render_template("register.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
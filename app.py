import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
app.secret_key = "my_password"


app.config["MONGO_DBNAME"] = 'sequencingMetricsDB'
app.config["MONGO_URI"] = 'mongodb+srv://seqMetRoot:seqMetR00tUser@sequencingmetricsdb-kpu2s.mongodb.net/sequencingMetricsDB?retryWrites=true&w=majority'


mongo = PyMongo(app)

"""
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        flash("Thanks {}, your data has been entered successfully".format(
            request.form["name"]))

    return render_template("index.html", metrics=mongo.db.seqMetCol.find())
"""

@app.route("/", methods=["GET", "POST"])
def index():
    """Main page with instructions"""
    if request.method == "POST":
        flash("Thanks {}, your data has been entered successfully".format(
            request.form["username"]
        ))
        session["username"] = request.form["username"]

    if "username" in session:
        return redirect(url_for("username", username=session["username"]))

    return render_template("index.html", metrics=mongo.db.seqMetCol.find())


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """ Add new user to database """
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    users = mongo.db.users
    allUsers = users.find({}, {'user:1', '_id:0'})
    if request.method == "POST":
        for user in allUsers:
            if user == request.form.get("username"):
                print("username already exists, please enter a unique username")
            else:
                newuser = request.form.get('newUsername')
                users.insert_one({'user':newuser, 'member':'user', 'joined':{'date':date, 'time':time}})
                return redirect(url_for('index'))
    return render_template("signup.html")


@app.route("/user/<username>", methods=["GET", "POST"])
def username(username):
    """Add and display chat messages"""
    metricsdb = mongo.db.seqMetCol
    if request.method == "POST":
        # session["username"] = request.form["username"]
        # username = session["username"]
        # username = request.form.get("name")
        # name = username
        pool = request.form.get("pool")
        yields = request.form.get("yield")
        clusterDensity = request.form.get("clusterDensity")
        passFilter = request.form.get("passFilter")
        q30 = request.form.get("q30")
        session.clear()
        run = {
            'user': username,
            'pool': pool,
            'yield': yields,
            'clusterDensity': clusterDensity,
            'passFilter': passFilter,
            'q30': q30
            }
        metricsdb.insert(run)
        # metrics.insert_one(request.form.to_dict())
        return redirect(url_for("username", username=username))

    session.clear()
    return render_template("user.html", username=username)
    # return render_template("user.html")


@app.route('/runs')
def runs():
    return render_template("runs.html", metrics=mongo.db.seqMetCol.find())


@app.route('/chemistry')
def chemistry():
    return render_template("chemistry.html")


@app.route('/experiments')
def experiments():
    return render_template("experiments.html")


@app.route('/users')
def users():
    return render_template("users.html")


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)

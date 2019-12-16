import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = "my_password"


app.config["MONGO_DBNAME"] = 'sequencingMetricsDB'
app.config["MONGO_URI"] = 'mongodb+srv://seqMetRoot:seqMetR00tUser@sequencingmetricsdb-kpu2s.mongodb.net/sequencingMetricsDB?retryWrites=true&w=majority'


mongo = PyMongo(app)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        flash("Thanks {}, your data has been entered successfully".format(
            request.form["name"]))

    return render_template("index.html", metrics=mongo.db.seqMetCol.find())

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

"""
@app.route("/")
def index():
    return render_template("index.html", metrics=mongo.db.seqMetCol.find())
"""

"""
@app.route("/get_metrics")
def getMetrics():
    return render_template("get-metrics.html", metrics=mongo.db.seqMetCol.find())
"""


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

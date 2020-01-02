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


def getExperiment(experimentParameter):
    data =list(mongo.db.seqMetCol.aggregate([
        {
            '$match': {
                # 'experiment': {'$exists': 'true'}
                'experiment': experimentParameter
            }
        },
        {
            '$group': {
                '_id': 'null',
                'count': { '$sum': 1 },
            }
        }
    ]))
    return data


def getUserExperiment(experiment, user):
    data = list(mongo.db.seqMetCol.aggregate([
    # data = mongo.db.seqMetCol.aggregate([
        {
            '$match': {
                '$and': [ {'user': user}, {'experiment': experiment} ]
            }
        },
        {
            '$group': {
                '_id': 'null',
                'count': { '$sum': 1 },
            }
        }
    ]))
    if data == []:
        data = [{'count': 0}]
    return data


def getChemistry(chemistryParameter):
    data = list(mongo.db.seqMetCol.aggregate([
        {
            '$match': {
                'chemistry': chemistryParameter
            }
        },
        {
            '$group': {
                '_id': 'null',
                'count': { '$sum': 1 },
            }
        }
    ]))
    return data


def getAllData(runParameter):
    PrefixDollarToRunParameter = "${}".format(runParameter)
    data = mongo.db.seqMetCol.aggregate([
        {
            '$match': {
                'user': {'$exists': 'true'}
            }
        },
        {
            '$group': {
                '_id': 'null',
                'count': { '$sum': 1 },
                'average': {'$avg': PrefixDollarToRunParameter},
                'minimum': {'$min': PrefixDollarToRunParameter},
                'maximum': {'$max': PrefixDollarToRunParameter}
            }
        }  
    ])
    return data

def getUserData(runParameter, user):
    PrefixDollarToRunParameter = "${}".format(runParameter)
    data = mongo.db.seqMetCol.aggregate([
        {
            '$match': {
                'user': user
            }
        },
        {
            '$group': {
                '_id': 'null',
                'count': { '$sum': 1 },
                'average': {'$avg': PrefixDollarToRunParameter},
                'minimum': {'$min': PrefixDollarToRunParameter},
                'maximum': {'$max': PrefixDollarToRunParameter}
            }
        }  
    ])
    return data

@app.route("/")
def index():
    """Display data for all users"""
    genome = getExperiment("Genome")[0]['count']
    exome = getExperiment("Exome")[0]['count']
    capture = getExperiment("Capture")[0]['count']
    high300=getChemistry("High300")[0]['count']
    mid300=getChemistry("Mid300")[0]['count']
    mid150=getChemistry("Mid150")[0]['count']
    yields = getAllData("yield")
    clusterDensity = getAllData("clusterDensity")
    passFilter = getAllData("passFilter")
    q30 = getAllData("q30")

    qcData = {
        'genome': genome,
        'exome': exome,
        'capture': capture,
        'high300': high300,
        'mid300': mid300,
        'mid150': mid150,
        'yields': yields,
        'clusterDensity': clusterDensity,
        'passFilter': passFilter,
        'q30': q30
    }

    return render_template("index.html", qcData=qcData)


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log in with username """
    # session.clear()
    users = mongo.db.users
    if request.method == "POST":
        username = request.form.get("username")
        for user in users.find({}, {'user': 1, '_id': 0}):
            if user.get('user') == username:
                session["username"] = username
        if "username" in session:
            return redirect(url_for("username", username=session["username"]))
        else:
            flash("The username '{}' doesn't exist, please try a different username".format(username))
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """ Add new user to database """
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    users = mongo.db.users
    if request.method == "POST":
        for user in users.find({}, {'user': 1, '_id': 0}):
            if user.get('user') == request.form.get("newUsername"):
                print("username already exists, please enter a unique username")
                return redirect(url_for('index'))                
            else:
                newuser = request.form.get('newUsername')
                users.insert_one({'user':newuser, 'member':'user', 'joined':{'date':date, 'time':time}})
                return redirect(url_for('index'))
    return render_template("signup.html")


@app.route("/user/<username>", methods=["GET", "POST"])
def username(username):
    """ Displays data for individual users & adds new runs """
    title = "WELCOME {}".format(username.upper())
    runs = mongo.db.seqMetCol
    if request.method == "POST":
        pool = request.form.get("pool")
        yields = request.form.get("yield")
        clusterDensity = request.form.get("clusterDensity")
        passFilter = request.form.get("passFilter")
        q30 = request.form.get("q30")
        experiment = request.form.get("experiment")
        chemistry = request.form.get("chemistry")
        comment = request.form.get("comment")
        session.clear()
        run = {
            'user': username,
            'pool': pool,
            'yield': yields,
            'clusterDensity': clusterDensity,
            'passFilter': passFilter,
            'q30': q30,
            'experiment': experiment,
            'chemistry': chemistry,
            'comment': comment
        }
        runs.insert_one(run)
        return redirect(url_for("username", username=username))

    genome = getUserExperiment("Genome", username)[0]['count']
    exome = getUserExperiment("Exome", username)[0]['count']
    capture = getUserExperiment("Capture", username)[0]['count']
    high300=getChemistry("High300")[0]['count']
    mid300=getChemistry("Mid300")[0]['count']
    mid150=getChemistry("Mid150")[0]['count']
    yields = getAllData("yield")
    clusterDensity = getUserData("clusterDensity", username)
    passFilter = getUserData("passFilter", username)
    q30 = getUserData("q30", username)

    qcData = {
        'genome': genome,
        'exome': exome,
        'capture': capture,
        'high300': high300,
        'mid300': mid300,
        'mid150': mid150,
        'yields': yields,
        'clusterDensity': clusterDensity,
        'passFilter': passFilter,
        'q30': q30
    }
    session.clear()
    return render_template("user.html", title=title, qcData=qcData)


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

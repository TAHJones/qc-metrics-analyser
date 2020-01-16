import os
from flask import Flask, render_template, redirect, request, url_for, flash, session, json
from flask_pymongo import PyMongo
# from bson.objectid import ObjectId
from datetime import datetime


app = Flask(__name__)
app.secret_key = "my_password"


app.config["MONGO_DBNAME"] = 'sequencingMetricsDB'
app.config["MONGO_URI"] = 'mongodb+srv://seqMetRoot:seqMetR00tUser@sequencingmetricsdb-kpu2s.mongodb.net/sequencingMetricsDB?retryWrites=true&w=majority'


mongo = PyMongo(app)


def getExperiment(experiment):
    data =list(mongo.db.seqMetCol.aggregate([
        {
            '$match': {
                # 'experiment': {'$exists': 'true'}
                'experiment': experiment
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


def getChemistry(chemistry):
    data = list(mongo.db.seqMetCol.aggregate([
        {
            '$match': {
                'chemistry': chemistry
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

def getUserChemistry(chemistry, user):
    data = list(mongo.db.seqMetCol.aggregate([
        {
            '$match': {
                '$and': [ {'user': user}, {'chemistry': chemistry} ]
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

def getDataSummary(param):
    dollarParam = "${}".format(param)
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
                'average': {'$avg': dollarParam},
                'minimum': {'$min': dollarParam},
                'maximum': {'$max': dollarParam}
            }
        }  
    ])
    return data

def getUserDataSummary(param, user):
    dollarParam = "${}".format(param)
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
                'average': {'$avg': dollarParam},
                'minimum': {'$min': dollarParam},
                'maximum': {'$max': dollarParam}
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
    yields = getDataSummary("yield")
    clusterDensity = getDataSummary("clusterDensity")
    passFilter = getDataSummary("passFilter")
    q30 = getDataSummary("q30")

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
    users = mongo.db.users
    if request.method == "POST":
        session.clear()
        username = request.form.get("username")
        for user in users.find({}, {'user': 1, '_id': 0}):
            if user.get('user') == username:
                session["username"] = username
        if "username" in session:
            print(session["username"])
            return redirect(url_for("user", username=session["username"]))
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
                flash("username already exists, please enter a unique username")
                return redirect(url_for('index'))                
            else:
                newuser = request.form.get('newUsername')
                users.insert_one({'user':newuser, 'member':'user', 'joined':{'date':date, 'time':time}})
                return redirect(url_for('index'))
    return render_template("signup.html")


@app.route("/user/<username>")
def user(username):
    """ Displays data for individual users & adds new runs """
    username = username 
    title = "WELCOME {}".format(username.upper())
    session["title"] = title
    genome = getUserExperiment("Genome", username)[0]['count']
    exome = getUserExperiment("Exome", username)[0]['count']
    capture = getUserExperiment("Capture", username)[0]['count']
    high300=getUserChemistry("High300", username)[0]['count']
    mid300=getUserChemistry("Mid300", username)[0]['count']
    mid150=getUserChemistry("Mid150", username)[0]['count']
    yields = getDataSummary("yield")
    clusterDensity = getUserDataSummary("clusterDensity", username)
    passFilter = getUserDataSummary("passFilter", username)
    q30 = getUserDataSummary("q30", username)
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
    return render_template("user.html", title=title, qcData=qcData, username=username)


@app.route("/view-user-runs", methods=["GET", "POST"])
def viewUserRuns():
    username = session["username"]
    if request.method == "POST":
        if request.form['formButton'] == "userRun":
            poolNumber = int(request.form.get("poolNumber"))
            session["poolNumber"] = poolNumber
            userRun = list(mongo.db.seqMetCol.find(
                {'user': username, 'pool': poolNumber}, { '_id': 0 }))
            if userRun == []:
                flash('No Runs of that type were found')
                userRun = [{
                            'pool': 0,
                            'yield': 0,
                            'clusterDensity': 0,
                            'passFilter': 0,
                            'q30': 0,
                            'experiment': 0,
                            'chemistry': 0
                            }]
            session["userRun"] = userRun[0]
            return render_template("view-user-runs.html",
                                    username=username,
                                    title=session["title"],
                                    userRun=userRun,
                                    pageLocation=json.dumps("userRun"))

        elif request.form['formButton'] == 'userRuns':
            minYield = int(request.form.get("minYield"))
            maxYield = int(request.form.get("maxYield"))
            minClusterDensity = int(request.form.get("minClusterDensity"))
            maxClusterDensity = int(request.form.get("maxClusterDensity"))
            minPassFilter = int(request.form.get("minPassFilter"))
            maxPassFilter = int(request.form.get("maxPassFilter"))
            minq30 = int(request.form.get("minq30"))
            maxq30 = int(request.form.get("maxq30"))
            experiment = request.form.get("experiment")
            chemistry = request.form.get("chemistry")

            if chemistry == "All" and experiment == "All":
                userData = list(mongo.db.seqMetCol.find({
                    '$and': [
                        {'user': username},
                        {'$and': [{'yield': {'$gt': minYield}}, {'yield': {'$lt': maxYield}}]},
                        {'$and': [{'clusterDensity': {'$gt': minClusterDensity}}, {'clusterDensity': {'$lt': maxClusterDensity}}]},
                        {'$and': [{'passFilter': {'$gt': minPassFilter}}, {'passFilter': {'$lt': maxPassFilter}}]},
                        {'$and': [{'q30': {'$gt': minq30}}, {'q30': {'$lt': maxq30}}]}
                    ]
                }, { '_id': 0 }))
            elif chemistry != "All" and experiment == "All":
                userData = list(mongo.db.seqMetCol.find({
                    '$and': [
                        {'user': username},
                        {'$and': [{'yield': {'$gt': minYield}}, {'yield': {'$lt': maxYield}}]},
                        {'$and': [{'clusterDensity': {'$gt': minClusterDensity}}, {'clusterDensity': {'$lt': maxClusterDensity}}]},
                        {'$and': [{'passFilter': {'$gt': minPassFilter}}, {'passFilter': {'$lt': maxPassFilter}}]},
                        {'$and': [{'q30': {'$gt': minq30}}, {'q30': {'$lt': maxq30}}]},
                        {'chemistry': chemistry }
                    ]
                }, { '_id': 0 }))
            elif chemistry == "All" and experiment != "All":
                userData = list(mongo.db.seqMetCol.find({
                    '$and': [
                        {'user': username},
                        {'$and': [{'yield': {'$gt': minYield}}, {'yield': {'$lt': maxYield}}]},
                        {'$and': [{'clusterDensity': {'$gt': minClusterDensity}}, {'clusterDensity': {'$lt': maxClusterDensity}}]},
                        {'$and': [{'passFilter': {'$gt': minPassFilter}}, {'passFilter': {'$lt': maxPassFilter}}]},
                        {'$and': [{'q30': {'$gt': minq30}}, {'q30': {'$lt': maxq30}}]},
                        {'experiment': experiment }
                    ]
                }, { '_id': 0 }))
            elif chemistry != "All" and experiment != "All":
                userData = list(mongo.db.seqMetCol.find({
                    '$and': [
                        {'user': username},
                        {'$and': [{'yield': {'$gt': minYield}}, {'yield': {'$lt': maxYield}}]},
                        {'$and': [{'clusterDensity': {'$gt': minClusterDensity}}, {'clusterDensity': {'$lt': maxClusterDensity}}]},
                        {'$and': [{'passFilter': {'$gt': minPassFilter}}, {'passFilter': {'$lt': maxPassFilter}}]},
                        {'$and': [{'q30': {'$gt': minq30}}, {'q30': {'$lt': maxq30}}]},
                        {'experiment': experiment },
                        {'chemistry': chemistry } 
                    ]
                }, { '_id': 0 }))

            if userData == []:
                flash('No Runs of that type were found')
                userData = [{
                            'run': 0,
                            'pool': 0,
                            'yield': 0,
                            'clusterDensity': 0,
                            'passFilter': 0,
                            'q30': 0
                            }]

            return render_template("view-user-runs.html",
                                    username=username,
                                    title=session["title"],
                                    userData=userData,
                                    pageLocation=json.dumps("userRuns"))
    return render_template("view-user-runs.html",
                            username=username,
                            title=session["title"],
                            pageLocation=json.dumps("userForm"))


@app.route("/add-user-run", methods=["GET", "POST"])
def addUserRun():
    """  Add new run to database """
    username = session["username"]
    runs = mongo.db.seqMetCol
    if request.method == "POST":
        pool = int(request.form.get("pool"))
        yields = int(request.form.get("yield"))
        clusterDensity = int(request.form.get("clusterDensity"))
        passFilter = int(request.form.get("passFilter"))
        q30 = int(request.form.get("q30"))
        experiment = request.form.get("experiment")
        chemistry = request.form.get("chemistry")
        comment = request.form.get("comment")
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
        return redirect(url_for("addUserRun", username=username, title=session["title"]))
    return render_template("add-user-run.html", username=username, title=session["title"])


@app.route("/delete-user-run")
def deleteUserRun():
    username = session["username"]
    poolNumber = int(request.args.get("poolNumber"))
    runs=mongo.db.seqMetCol
    runs.remove({'user': username, 'pool': poolNumber})
    return render_template("delete-user-run.html", title=session["title"])


@app.route("/update-user-run", methods=["GET", "POST"])
def updateUserRun():
    username = session["username"]
    title = request.args.get("title")
    runs = mongo.db.seqMetCol
    existingPoolNumber = int(session["userRun"].get("pool"))
    if request.method == "POST":
        newPoolNumber = int(request.form.get("pool"))
        yields = int(request.form.get("yield"))
        clusterDensity = int(request.form.get("clusterDensity"))
        passFilter = int(request.form.get("passFilter"))
        q30 = int(request.form.get("q30"))
        experiment = request.form.get("experiment")
        chemistry = request.form.get("chemistry")
        comment = request.form.get("comment")
        updateRun = {
            'pool': newPoolNumber,
            'yield': yields,
            'clusterDensity': clusterDensity,
            'passFilter': passFilter,
            'q30': q30,
            'experiment': experiment,
            'chemistry': chemistry,
            'comment': comment
        }
        runs.update_one( {'user': username, 'pool': existingPoolNumber }, {'$set': updateRun })
        return redirect(url_for("viewUserRuns", title=title))

    return render_template("update-user-run.html", userRun=json.dumps(session.get("userRun")))


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)

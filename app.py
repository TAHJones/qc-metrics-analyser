import os
from flask import Flask, render_template, redirect, request, url_for, flash, session, json
from flask_pymongo import PyMongo
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
    """Display summary run data for all users"""
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
    graphData = list(mongo.db.seqMetCol.find({}, { 'pool': 1, 'yield': 1, 'passFilter': 1, 'clusterDensity': 1, 'q30': 1, 'chemistry': 1, 'experiment':1, '_id': 0 }))
    pools = []
    yields = []
    clusterDensity = []
    passFilter = []
    q30 = []
    chemistries = []
    experiments = []

    for data in graphData:
        poolNumber = "Pool_{}".format(data["pool"])
        pools.append(poolNumber)
        yields.append(data["yield"])
        clusterDensity.append(data["clusterDensity"])
        passFilter.append(data["passFilter"])
        q30.append(data["q30"])
        chemistries.append(data["chemistry"])
        experiments.append(data["experiment"])

    labels=json.dumps(pools)
    yields = json.dumps(yields)
    clusterDensity = json.dumps(clusterDensity)
    passFilter = json.dumps(passFilter)
    q30 = json.dumps(q30)

    return render_template("index.html",
                            qcData=qcData,
                            labels=labels, 
                            yields=yields,
                            clusterDensity=clusterDensity,
                            passFilter=passFilter,
                            q30=q30)


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
                member = users.find_one({'user': username}, { '_id': 0 }).get("member")
        if "username" in session and member == "admin":
            return redirect(url_for("adminOrUser", username=session["username"]))
        elif "username" in session and member == "user":    
            return redirect(url_for("user", username=session["username"]))
        else:
            flash("The username '{}' doesn't exist, please try a different username".format(username))
    return render_template("login.html")


@app.route("/logout")
def logout():
    """ log out user and return to homepage """
    session.clear()
    return redirect(url_for('index'))


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
                return redirect(url_for('signup'))                
        newuser = request.form.get('newUsername')
        users.insert_one({'user':newuser, 'member':'user', 'joined':{'date':date, 'time':time}})
        flash("congratulations your username has been added to the database")
        return redirect(url_for('signup'))
    return render_template("signup.html")


@app.route("/admin-or-user/<username>")
def adminOrUser(username):
    """ If user had admin rights give option to login as admin or user """
    username = username
    title = "WELCOME {}".format(username.upper())
    session["title"] = title
    return render_template("admin-or-user.html", title=title, username=username)


@app.route("/admin/<username>")
def admin(username):
    """ admin page for removing & updating user & sequencing run data """
    username = username
    return render_template("admin.html", title=session["title"], username=username)


@app.route("/admin-select-runs", methods=["GET", "POST"])
def adminSelectRuns():
    """ select user runs to view, remove & update """
    username = session["username"]
    if request.method == "POST" and request.form['formButton'] == 'userRuns':
        selectedUser = request.form.get("username")
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
            userRuns = list(mongo.db.seqMetCol.find({
                '$and': [
                    {'user': selectedUser},
                    {'$and': [{'yield': {'$gt': minYield}}, {'yield': {'$lt': maxYield}}]},
                    {'$and': [{'clusterDensity': {'$gt': minClusterDensity}}, {'clusterDensity': {'$lt': maxClusterDensity}}]},
                    {'$and': [{'passFilter': {'$gt': minPassFilter}}, {'passFilter': {'$lt': maxPassFilter}}]},
                    {'$and': [{'q30': {'$gt': minq30}}, {'q30': {'$lt': maxq30}}]}
                ]
            }, { '_id': 0 }))
        elif chemistry != "All" and experiment == "All":
            userRuns = list(mongo.db.seqMetCol.find({
                '$and': [
                    {'user': selectedUser},
                    {'$and': [{'yield': {'$gt': minYield}}, {'yield': {'$lt': maxYield}}]},
                    {'$and': [{'clusterDensity': {'$gt': minClusterDensity}}, {'clusterDensity': {'$lt': maxClusterDensity}}]},
                    {'$and': [{'passFilter': {'$gt': minPassFilter}}, {'passFilter': {'$lt': maxPassFilter}}]},
                    {'$and': [{'q30': {'$gt': minq30}}, {'q30': {'$lt': maxq30}}]},
                    {'chemistry': chemistry }
                ]
            }, { '_id': 0 }))
        elif chemistry == "All" and experiment != "All":
            userRuns = list(mongo.db.seqMetCol.find({
                '$and': [
                    {'user': selectedUser},
                    {'$and': [{'yield': {'$gt': minYield}}, {'yield': {'$lt': maxYield}}]},
                    {'$and': [{'clusterDensity': {'$gt': minClusterDensity}}, {'clusterDensity': {'$lt': maxClusterDensity}}]},
                    {'$and': [{'passFilter': {'$gt': minPassFilter}}, {'passFilter': {'$lt': maxPassFilter}}]},
                    {'$and': [{'q30': {'$gt': minq30}}, {'q30': {'$lt': maxq30}}]},
                    {'experiment': experiment }
                ]
            }, { '_id': 0 }))
        elif chemistry != "All" and experiment != "All":
            userRuns = list(mongo.db.seqMetCol.find({
                '$and': [
                    {'user': selectedUser},
                    {'$and': [{'yield': {'$gt': minYield}}, {'yield': {'$lt': maxYield}}]},
                    {'$and': [{'clusterDensity': {'$gt': minClusterDensity}}, {'clusterDensity': {'$lt': maxClusterDensity}}]},
                    {'$and': [{'passFilter': {'$gt': minPassFilter}}, {'passFilter': {'$lt': maxPassFilter}}]},
                    {'$and': [{'q30': {'$gt': minq30}}, {'q30': {'$lt': maxq30}}]},
                    {'experiment': experiment },
                    {'chemistry': chemistry } 
                ]
            }, { '_id': 0 }))
        session["selectedUser"] = selectedUser

        if userRuns == []:
            flash('No Runs of that type were found')
            userRuns = [{
                        'run': 0,
                        'pool': 0,
                        'yield': 0,
                        'clusterDensity': 0,
                        'passFilter': 0,
                        'q30': 0
                        }]
        return render_template("admin-select-runs.html",
                                username=username,
                                title=session["title"],
                                pageLocation=json.dumps("userRuns"),
                                selectedUser=selectedUser,
                                userRuns=userRuns)
    elif request.method == "POST" and request.form['formButton'] == 'userRun':
        selectedPoolNumber = int(request.form.get("selectedPoolNumber"))
        session["selectedPoolNumber"] = selectedPoolNumber
        selectedUser = session["selectedUser"]
        selectedUserRun = list(mongo.db.seqMetCol.find(
            {'user': selectedUser, 'pool': selectedPoolNumber}, { '_id': 0 }))
        if selectedUserRun == []:
            flash('No Runs of that type were found')
            selectedUserRun = [{
                        'pool': 0,
                        'yield': 0,
                        'clusterDensity': 0,
                        'passFilter': 0,
                        'q30': 0,
                        'experiment': 0,
                        'chemistry': 0
                        }]
        session["selectedUserRun"] = selectedUserRun
        return render_template("admin-select-runs.html",
                                username=username,
                                title=session["title"],
                                pageLocation=json.dumps("userRun"),
                                selectedPoolNumber=selectedPoolNumber,
                                selectedUser=selectedUser,
                                selectedUserRun=selectedUserRun)
    users = mongo.db.users
    userList = list(users.find({}, {'user': 1, '_id': 0}))
    session["userList"] = userList
    return render_template("admin-select-runs.html",
                                username=username,
                                title=session["title"],
                                pageLocation=json.dumps("userForm"),
                                userList=userList)

def createDropDownList(dataList, currentSelection):
    dropDownList = {}
    for data in dataList:
        if data == currentSelection:
            dropDownList["selectedItem"] = data
        elif data != currentSelection and "unselectedItem1" not in dropDownList:
                dropDownList["unselectedItem1"] = data
        else:
            dropDownList["unselectedItem2"] = data
    return dropDownList


@app.route("/admin-update-run", methods=["GET", "POST"])
def adminUpdateRun():
    """  Allows administrator to update runs for selected user """
    selectedUser = session["selectedUser"]
    existingPoolNumber = session["selectedPoolNumber"]
    selectedUserRun = session["selectedUserRun"]
    existingExperiment = selectedUserRun[0].get("experiment")
    existingChemistry = selectedUserRun[0].get("chemistry")
    experiments = ["Genome", "Exome", "Capture"]
    chemistries = ["High300", "Mid300", "Mid150"]
    experimentList = createDropDownList(experiments, existingExperiment)
    chemistryList = createDropDownList(chemistries, existingChemistry)

    if request.method == "POST":
        newUserName = request.form.get("name")
        newPoolNumber = int(request.form.get("pool"))
        yields = int(request.form.get("yield"))
        clusterDensity = int(request.form.get("clusterDensity"))
        passFilter = int(request.form.get("passFilter"))
        q30 = int(request.form.get("q30"))
        experiment = request.form.get("experiment")
        chemistry = request.form.get("chemistry")
        comment = request.form.get("comment")
        updateRun = {
            'user': newUserName,
            'pool': newPoolNumber,
            'yield': yields,
            'clusterDensity': clusterDensity,
            'passFilter': passFilter,
            'q30': q30,
            'experiment': experiment,
            'chemistry': chemistry,
            'comment': comment
        }
        selectedUserRun = [updateRun]
        runs = mongo.db.seqMetCol
        runs.update_one( {'user': selectedUser, 'pool': existingPoolNumber }, {'$set': updateRun })
        flash("Pool_{} has been successfully updated".format(existingPoolNumber))
        experimentList = createDropDownList(experiments, experiment)
        chemistryList = createDropDownList(chemistries, chemistry)
        return render_template("admin-update-run.html",
                                title=session["title"],
                                existingPoolNumber=existingPoolNumber,
                                userRun=selectedUserRun,
                                chemistryList=chemistryList, 
                                experimentList=experimentList, 
                                pageLocation=json.dumps("userRun"))
    return render_template("admin-update-run.html",
                            title=session["title"],
                            existingPoolNumber=existingPoolNumber,
                            userRun=selectedUserRun,
                            chemistryList=chemistryList,
                            experimentList=experimentList,
                            pageLocation=json.dumps("userForm"))


@app.route("/admin-delete-run", methods=["GET", "POST"])
def adminDeleteRun():
    """  Delete selected run from database """
    username = session["username"]
    selectedUserRun = session["selectedUserRun"]
    selectedPoolNumber = session["selectedPoolNumber"]
    if request.method == "POST":
        radio = request.form.get("radio")
        if radio == 'yes':
            deletedRun = {
                'pool': 'Deleted',
                'yield': 'Deleted',
                'clusterDensity': 'Deleted',
                'passFilter': 'Deleted',
                'q30': 'Deleted',
                'experiment': 'Deleted',
                'chemistry': 'Deleted'
            }
            # mongo.db.seqMetCol.remove({'pool': selectedUserRun})
            selectedUserRun = [deletedRun]
            pageLocation=json.dumps("runDeleted")
            flash("Pool_{} has been successfully deleted".format(selectedPoolNumber))
        elif radio == 'no':
            flash("To delete Pool_{} select 'Yes' then click 'Delete'".format(selectedPoolNumber))
            pageLocation=json.dumps("deleteRunForm")
        return render_template("admin-delete-run.html",
                                    username=username,
                                    title=session["title"],
                                    pageLocation=pageLocation,
                                    selectedUserRun=selectedUserRun)
    return render_template("admin-delete-run.html",
                                username=username,
                                title=session["title"],
                                pageLocation=json.dumps("deleteRunForm"),
                                selectedUserRun=selectedUserRun)


@app.route("/admin-select-user", methods=["GET", "POST"])
def adminSelectUser():
    """ select users to view, remove & update """
    username = session["username"]
    users = mongo.db.users
    if request.method == "POST":
        user = request.form.get("user")
        selectedUser = list(users.find({'user': user}, { '_id': 0 }))
        session["selectedUser"] = selectedUser
        selectedUserName = selectedUser[0].get("user")
        session["selectedUserName"] = selectedUserName
        return render_template("admin-select-user.html",
                                    username=username,
                                    title=session["title"],
                                    pageLocation=json.dumps("viewUser"),
                                    selectedUser=selectedUser,
                                    selectedUserName=selectedUserName)
    userList = list(users.find({}, {'user': 1, '_id': 0}))
    return render_template("admin-select-user.html",
                                username=username,
                                title=session["title"],
                                pageLocation=json.dumps("userForm"),
                                userList=userList)


@app.route("/admin-update-user", methods=["GET", "POST"])
def adminUpdateUser():
    """ select user to view, delete & update """
    username = session["username"]
    selectedUser = session["selectedUser"]
    users = mongo.db.users
    selectedUserName = session["selectedUserName"]
    if request.method == "POST":
        user = request.form.get("user")
        member = request.form.get("member")
        date = request.form.get("date")
        time = request.form.get("time")
        updateUser = {
            'user': user,
            'member': member,
            'joined': {'date': date, 'time': time}
        }
        users.update_one( {'user': selectedUserName}, {'$set': updateUser})
        flash("User account for {} has been successfully updated".format(selectedUserName))

        selectedUser = [updateUser]
        return render_template("admin-update-user.html",
                                    username=username,
                                    title=session["title"],
                                    selectedUser=selectedUser)
    return render_template("admin-update-user.html",
                                username=username,
                                title=session["title"],
                                selectedUser=selectedUser)


@app.route("/admin-delete-user", methods=["GET", "POST"])
def adminDeleteUser():
    """ select user to view, delete & update """
    username = session["username"]
    selectedUser = session["selectedUser"]
    selectedUserName = session["selectedUserName"]
    
    if request.method == "POST":
        radio = request.form.get("radio")
        if radio == 'yes':
            updateUser = {
                'user': 'Deleted',
                'member': 'Deleted',
                'joined': {'date': 'Deleted', 'time': 'Deleted'}
            }
            selectedUser = [updateUser]
            # users = mongo.db.users
            # users.remove({'user': selectedUserName})
            pageLocation=json.dumps("userDeleted")
            flash("User account for {} has been successfully deleted".format(selectedUserName))
        elif radio == 'no':
            flash("To delete user account for {} select 'Yes' then click 'Delete'".format(selectedUserName))
            pageLocation=json.dumps("deleteUserForm")
        return render_template("admin-delete-user.html",
                                    username=username,
                                    title=session["title"],
                                    pageLocation=pageLocation,
                                    selectedUser=selectedUser,
                                    selectedUserName=selectedUserName)
    return render_template("admin-delete-user.html",
                                username=username,
                                title=session["title"],
                                pageLocation=json.dumps("deleteUserForm"),
                                selectedUser=selectedUser,
                                selectedUserName=selectedUserName)

@app.route("/user/<username>")
def user(username):
    """ Display summary of run data for individual users """
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
    graphData = list(mongo.db.seqMetCol.find({ 'user': username }, { 'pool': 1, 'yield': 1, 'passFilter': 1, 'clusterDensity': 1, 'q30': 1, 'chemistry': 1, 'experiment':1, '_id': 0 }))
    pools = []
    yields = []
    clusterDensity = []
    passFilter = []
    q30 = []
    chemistries = []
    experiments = []

    for data in graphData:
        poolNumber = "Pool_{}".format(data["pool"])
        pools.append(poolNumber)
        yields.append(data["yield"])
        clusterDensity.append(data["clusterDensity"])
        passFilter.append(data["passFilter"])
        q30.append(data["q30"])
        chemistries.append(data["chemistry"])
        experiments.append(data["experiment"])

    labels=json.dumps(pools)
    yields = json.dumps(yields)
    clusterDensity = json.dumps(clusterDensity)
    passFilter = json.dumps(passFilter)
    q30 = json.dumps(q30)
    return render_template("user.html",
                            title=title,
                            username=username,
                            qcData=qcData,
                            labels=labels, 
                            yields=yields,
                            clusterDensity=clusterDensity,
                            passFilter=passFilter,
                            q30=q30)


@app.route("/view-user-runs", methods=["GET", "POST"])
def viewUserRuns():
    """  view all user runs or select individual run to delete or update """
    username = session["username"]
    userRunList = list(mongo.db.seqMetCol.find({ 'user': username }, { 'pool': 1, '_id': 0 }))
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
            session["userRun"] = userRun
            return render_template("view-user-runs.html",
                                    username=username,
                                    title=session["title"],
                                    userRun=userRun,
                                    pageLocation=json.dumps("userRun"),
                                    userRunList=userRunList)

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
                                    pageLocation=json.dumps("userRuns"),
                                    userRunList=userRunList)
    return render_template("view-user-runs.html",
                            username=username,
                            title=session["title"],
                            pageLocation=json.dumps("userForm"),
                            userRunList=userRunList)


@app.route("/add-user-run", methods=["GET", "POST"])
def addUserRun():
    """  Add new run to database """
    username = session["username"]
    runs = mongo.db.seqMetCol
    if request.method == "POST":
        for run in runs.find({}, { 'pool': 1, '_id': 0 }):
            if run.get('pool') == int(request.form.get('pool')):
                flash("Pool already exists, please enter a unique pool number")
                return redirect(url_for("addUserRun", username=username, title=session["title"]))
        pool = int(request.form.get("pool"))
        yields = int(request.form.get("yield"))
        clusterDensity = int(request.form.get("clusterDensity"))
        passFilter = int(request.form.get("passFilter"))
        q30 = int(request.form.get("q30"))
        experiment = request.form.get("experiment")
        chemistry = request.form.get("chemistry")
        comment = request.form.get("comment")
        newRun = {
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
        runs.insert_one(newRun)
        flash("Pool_{} has been successfully added".format(pool))
        return redirect(url_for("addUserRun", username=username, title=session["title"]))
    return render_template("add-user-run.html", username=username, title=session["title"])


@app.route("/delete-user-run", methods=["GET", "POST"])
def deleteUserRun():
    """  Delete selected run from database """
    username = session["username"]
    poolNumber = session["poolNumber"]
    if request.method == "POST":
        radio = request.form.get("radio")
        if radio == 'yes':
            deletedRun = {
                'pool': 'Deleted',
                'yield': 'Deleted',
                'clusterDensity': 'Deleted',
                'passFilter': 'Deleted',
                'q30': 'Deleted',
                'experiment': 'Deleted',
                'chemistry': 'Deleted'
            }
            userRun = [deletedRun]
            mongo.db.seqMetCol.remove({'user': username, 'pool': poolNumber})
            pageLocation=json.dumps("runDeleted")
            flash("Pool_{} has been successfully deleted".format(poolNumber))
        elif radio == 'no':
            flash("To delete Pool_{} select 'Yes' then click 'Delete'".format(poolNumber))
            pageLocation=json.dumps("deleteRunForm")
            userRun=session["userRun"]
        return render_template("delete-user-run.html",
                                    username=username,
                                    title=session["title"],
                                    pageLocation=pageLocation,
                                    userRun=userRun)
    userRun=session["userRun"]
    return render_template("delete-user-run.html",
                                username=username,
                                title=session["title"],
                                pageLocation=json.dumps("deleteRunForm"),
                                userRun=userRun)


@app.route("/update-user-run", methods=["GET", "POST"])
def updateUserRun():
    """  Update selected run from database """
    username = session["username"]
    userRun = session["userRun"]
    existingPoolNumber = int(userRun[0].get("pool"))
    existingExperiment = userRun[0].get("experiment")
    existingChemistry = userRun[0].get("chemistry")
    experiments = ["Genome", "Exome", "Capture"]
    chemistries = ["High300", "Mid300", "Mid150"]
    experimentList = createDropDownList(experiments, existingExperiment)
    chemistryList = createDropDownList(chemistries, existingChemistry)
    if request.method == "POST":
        newUserName = request.form.get("user")
        newPoolNumber = int(request.form.get("pool"))
        yields = int(request.form.get("yield"))
        clusterDensity = int(request.form.get("clusterDensity"))
        passFilter = int(request.form.get("passFilter"))
        q30 = int(request.form.get("q30"))
        experiment = request.form.get("experiment")
        chemistry = request.form.get("chemistry")
        comment = request.form.get("comment")
        updateRun = {
            'user': newUserName,
            'pool': newPoolNumber,
            'yield': yields,
            'clusterDensity': clusterDensity,
            'passFilter': passFilter,
            'q30': q30,
            'experiment': experiment,
            'chemistry': chemistry,
            'comment': comment
        }
        userRun = [updateRun]
        session["userRun"] = userRun
        runs = mongo.db.seqMetCol
        runs.update_one( {'user': username, 'pool': existingPoolNumber }, {'$set': updateRun })
        flash("Pool_{} has been successfully updated".format(existingPoolNumber))
        experimentList = createDropDownList(experiments, experiment)
        chemistryList = createDropDownList(chemistries, chemistry)
        return render_template("update-user-run.html",
                                title=session["title"],
                                existingPoolNumber=existingPoolNumber,
                                userRun=userRun,
                                chemistryList=chemistryList, 
                                experimentList=experimentList) 
    return render_template("update-user-run.html",
                            title=session["title"],
                            existingPoolNumber=existingPoolNumber,
                            userRun=userRun,
                            chemistryList=chemistryList, 
                            experimentList=experimentList)


if __name__ == "__main__":
    # app.jinja_env.auto_reload = True
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)

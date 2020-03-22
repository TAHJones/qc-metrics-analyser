import os
from os import path
if path.exists("env.py"):
    import env
from flask import Flask, render_template, redirect, request, url_for, flash, session, json
from flask_pymongo import PyMongo
from datetime import datetime
from helpers import Helpers


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)


runs = mongo.db.seqMetCol
users = mongo.db.users


@app.route("/")
def index():
    """Display summary run data for all users"""
    runData = Helpers.getRunData(runs)
    experimentData = Helpers.getExperimentData(runs)
    linechartData = Helpers.getLinechartData(runs)
    return render_template("pages/index.html",
                            runData=runData,
                            experimentData=experimentData,
                            linechartData=linechartData)


@app.route("/pages/login", methods=["GET", "POST"])
def login():
    """ Log in with username. If username doesn't exist user is prompted to try another username.
    If user exists & has admin privileges they are directed to 'adminOrUser' page. If user exists
    & only has user privileges they are directed to 'user' page """
    if request.method == "POST":
        session.clear()
        username = request.form.get("username")
        for user in users.find({}, {'user': 1, '_id': 0}):
            if user.get('user') == username:
                session["username"] = username
                member = users.find_one({'user': username}, { '_id': 0 }).get("member")
        if "username" in session and member == "admin":
            session["admin"] = True
            return redirect(url_for("adminOrUser", username=session["username"]))
        elif "username" in session and member == "user":    
            session["admin"] = False
            return redirect(url_for("user", username=session["username"]))
        else:
            flash("The username '{}' doesn't exist, please try a different username".format(username))
    return render_template("pages/auth.html", active="login")


@app.route("/logout")
def logout():
    """ log out user and return to homepage """
    session.clear()
    return redirect(url_for('pages/index'))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """ Add new user to database. Check if username exists, if it does then user is prompted
    to try another username. If username doesn't exist add to database """
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    if request.method == "POST":
        for user in users.find({}, {'user': 1, '_id': 0}):
            if user.get('user') == request.form.get("newUsername"):
                flash("username already exists, please enter a unique username")
                return redirect(url_for('signup'))                
        newuser = request.form.get('newUsername')
        users.insert_one({'user':newuser, 'member':'user', 'joined':{'date':date, 'time':time}})
        flash("congratulations your username has been added to the database")
        return redirect(url_for('signup'))
    return render_template("pages/auth.html", active="signup")


@app.route("/admin-or-user/<username>")
def adminOrUser(username):
    """ If user had admin rights give option to login as admin or user """
    username = username
    title = "WELCOME {}".format(username.upper())
    session["title"] = title
    return render_template("pages/admin-or-user.html", title=title, username=username)


@app.route("/admin/<username>")
def admin(username):
    """ admin page for removing & updating user & sequencing run data """
    username = username
    return render_template("pages/admin.html", title=session["title"], username=username)


@app.route("/admin/select/runs", methods=["GET", "POST"])
def adminSelectRuns():
    """ select runs for individual users and then view, remove or update individual user runs """
    username = session["username"]
    if request.method == "POST" and request.form['formButton'] == 'userRuns':
        userRuns = Helpers.getUserRuns(runs)
        Helpers.checkUserRuns(userRuns)
        if userRuns != []:
            session["selectedUser"] = userRuns[0]["user"]
        return render_template("pages/admin-select-runs.html",
                                username=username,
                                title=session["title"],
                                pageLocation=json.dumps("userRuns"),
                                selectedUser=session["selectedUser"],
                                userRuns=userRuns)
    elif request.method == "POST" and request.form['formButton'] == 'userRun':
        selectedUser = session["selectedUser"]
        selectedUserRun = Helpers.getUserRun(runs, selectedUser)
        session["selectedUserRun"] = selectedUserRun
        selectedPoolNumber = selectedUserRun[0]["pool"]
        session["selectedPoolNumber"] = selectedPoolNumber
        return render_template("pages/admin-select-runs.html",
                                username=username,
                                title=session["title"],
                                pageLocation=json.dumps("userRun"),
                                selectedPoolNumber=selectedPoolNumber,
                                selectedUser=selectedUser,
                                selectedUserRun=selectedUserRun)
    userList = Helpers.getUserList(users)
    session["userList"] = userList
    return render_template("pages/admin-select-runs.html",
                                username=username,
                                title=session["title"],
                                pageLocation=json.dumps("userForm"),
                                userList=userList)


@app.route("/manage/runs/update", methods=["GET", "POST"])
def updateRun():
    """  Allows administrator to update runs for selected user """
    if session["admin"] == True:
        userRun = session["selectedUserRun"]
    elif session["admin"] == False:
        userRun = session["userRun"]
    username = session["username"]
    existingPoolNumber = userRun[0]["pool"]
    existingChemistry = userRun[0]["chemistry"]
    existingExperiment = userRun[0]["experiment"]
    dropDownLists = Helpers.getDropDownLists(existingChemistry, existingExperiment)
    if request.method == "POST":
        if request.form["formName"] == "adminForm":
            selectedUser = session["selectedUser"]
            updatedRun = Helpers.updateUserRun(runs, existingPoolNumber, selectedUser)
        elif request.form["formName"] == "userForm":
            updatedRun = Helpers.updateUserRun(runs, existingPoolNumber, username)
        userRun = [updatedRun["userRun"]]
        message = updatedRun["message"]
        if userRun[0] == "error":
            flash(message)
            userRun = session["userRun"]
            return render_template("pages/update-run.html",
                                    username=username,
                                    title=session["title"],
                                    existingPoolNumber=existingPoolNumber,
                                    userRun=userRun,
                                    chemistryList=dropDownLists["chemistryList"], 
                                    experimentList=dropDownLists["experimentList"],
                                    page="update-run",
                                    admin=session["admin"])
        else:
            flash(message)
            session["userRun"] = userRun
            newChemistry = userRun[0]["chemistry"]
            newExperiment = userRun[0]["experiment"]
            dropDownLists = Helpers.getDropDownLists(newChemistry, newExperiment)
            return render_template("pages/update-run.html",
                                    username=username,
                                    title=session["title"],
                                    existingPoolNumber=existingPoolNumber,
                                    userRun=userRun,
                                    chemistryList=dropDownLists["chemistryList"], 
                                    experimentList=dropDownLists["experimentList"],
                                    page="update-run",
                                    admin=session["admin"]) 
    return render_template("pages/update-run.html",
                            username=username,
                            title=session["title"],
                            existingPoolNumber=existingPoolNumber,
                            userRun=userRun,
                            chemistryList=dropDownLists["chemistryList"], 
                            experimentList=dropDownLists["experimentList"],
                            page="update-run",
                            admin=session["admin"]) 


@app.route("/manage/runs/delete", methods=["GET", "POST"])
def deleteRun():
    admin = True
    """  Delete selected run from database """
    username = session["username"]
    if request.method == "POST":
        if request.form["formName"] == "adminForm":
            selectedPoolNumber = session["selectedPoolNumber"]
            deletedRun = Helpers.deleteUserRun(runs, selectedPoolNumber)
            userRun = deletedRun["userRun"]
            if userRun == None:
                userRun = session["selectedUserRun"]
        elif request.form["formName"] == "userForm":
            poolNumber = session["poolNumber"]
            deletedRun = Helpers.deleteUserRun(runs, poolNumber, username)
            userRun = deletedRun["userRun"]
            if userRun == None:
                userRun=session["userRun"]                
        message = deletedRun["message"]
        flash(message)
        pageLocation = deletedRun["pageLocation"]
        return render_template("pages/delete-run.html",
                                        username=username,
                                        title=session["title"],
                                        pageLocation=json.dumps(pageLocation),
                                        userRun=userRun,
                                        page = "delete-run",
                                        admin=admin)    
    pageLocation = "deleteRunForm"
    if admin == True:
        userRun = session["selectedUserRun"]
    else:
        userRun = session["userRun"]
    return render_template("pages/delete-run.html",
                                username=username,
                                title=session["title"],
                                pageLocation=json.dumps(pageLocation),
                                userRun=userRun,
                                page = "delete-run",
                                admin=admin)


@app.route("/admin/select/user", methods=["GET", "POST"])
def adminSelectUser():
    """ select users to view, remove & update """
    username = session["username"]
    if request.method == "POST":
        selectedUser = Helpers.adminSelectUser(users)
        session["selectedUser"] = selectedUser
        selectedUserName = selectedUser[0]["user"]
        session["selectedUserName"] = selectedUserName
        return render_template("pages/admin-select-user.html",
                                    username=username,
                                    title=session["title"],
                                    pageLocation=json.dumps("viewUser"),
                                    selectedUser=selectedUser,
                                    selectedUserName=selectedUserName)
    userList = Helpers.getUserList(users)
    return render_template("pages/admin-select-user.html",
                                username=username,
                                title=session["title"],
                                pageLocation=json.dumps("userForm"),
                                userList=userList)


@app.route("/admin/update/user", methods=["GET", "POST"])
def adminUpdateUser():
    """ select user to view, delete & update """
    username = session["username"]
    selectedUser = session["selectedUser"]
    selectedUserName = session["selectedUserName"]
    if request.method == "POST":
        updateUser = Helpers.adminUpdateUser(users, runs, selectedUserName)
        userData = updateUser["userData"]
        selectedUserName = userData["user"]
        message = updateUser["message"]
        flash(message)
        selectedUser = [userData]
        session["selectedUser"] = selectedUser
        session["selectedUserName"] = selectedUserName
        return render_template("pages/admin-update-user.html",
                                    username=username,
                                    title=session["title"],
                                    selectedUser=selectedUser)
    return render_template("pages/admin-update-user.html",
                                username=username,
                                title=session["title"],
                                selectedUser=selectedUser)


@app.route("/admin/delete/user", methods=["GET", "POST"])
def adminDeleteUser():
    """ select user to view, delete & update """
    username = session["username"]
    selectedUser = session["selectedUser"]
    selectedUserName = session["selectedUserName"]
    if request.method == "POST":
        deletedUser = Helpers.adminDeleteUser(users, runs, selectedUserName)
        userData = deletedUser["userData"]
        if userData == None:
            selectedUser = session["selectedUser"]
        else:
            selectedUser = [userData]
        message = deletedUser["message"]
        flash(message)
        pageLocation = deletedUser["pageLocation"]
        return render_template("pages/admin-delete-user.html",
                                    username=username,
                                    title=session["title"],
                                    pageLocation=json.dumps(pageLocation),
                                    selectedUser=selectedUser,
                                    selectedUserName=selectedUserName)
    return render_template("pages/admin-delete-user.html",
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
    runData = Helpers.getRunData(runs, username)
    experimentData = Helpers.getExperimentData(runs, username)
    linechartData = Helpers.getLinechartData(runs, username)
    return render_template("pages/user.html",
                            title=title,
                            username=username,
                            runData=runData,
                            experimentData=experimentData,
                            linechartData=linechartData)


@app.route("/view-user-runs", methods=["GET", "POST"])
def viewUserRuns():
    """  view all user runs or select individual run to delete or update """
    username = session["username"]
    userRunList = Helpers.getUserRunList(runs, username)
    if request.method == "POST":
        if request.form['formButton'] == "userRun":
            userRun = Helpers.getUserRun(runs, username)
            session["userRun"] = userRun
            session["poolNumber"] = userRun[0]["pool"]
            return render_template("pages/view-user-runs.html",
                                    username=username,
                                    title=session["title"],
                                    userRun=userRun,
                                    pageLocation=json.dumps("userRun"),
                                    userRunList=userRunList)
        elif request.form['formButton'] == 'userRuns':
            userRuns = Helpers.getUserRuns(runs, username)          
            Helpers.checkUserRuns(userRuns)
            return render_template("pages/view-user-runs.html",
                                    username=username,
                                    title=session["title"],
                                    userRuns=userRuns,
                                    pageLocation=json.dumps("userRuns"),
                                    userRunList=userRunList)
    return render_template("pages/view-user-runs.html",
                            username=username,
                            title=session["title"],
                            pageLocation=json.dumps("userForm"),
                            userRunList=userRunList)


@app.route("/add-user-run", methods=["GET", "POST"])
def addUserRun():
    """  Add new run to database """
    username = session["username"]
    if request.method == "POST":
        message = Helpers.addUserRun(runs, username)
        flash(message)
        return redirect(url_for("addUserRun", username=username, title=session["title"]))
    return render_template("pages/add-user-run.html", username=username, title=session["title"])


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)

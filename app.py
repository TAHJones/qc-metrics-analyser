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
    return render_template("index.html",
                            runData=runData,
                            experimentData=experimentData,
                            linechartData=linechartData)


@app.route("/login", methods=["GET", "POST"])
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
    """ select runs for individual users and then view, remove or update individual user runs """
    username = session["username"]
    if request.method == "POST" and request.form['formButton'] == 'userRuns':
        userRuns = Helpers.getUserRuns(runs)
        Helpers.checkUserRuns(userRuns)
        if userRuns != []:
            session["selectedUser"] = userRuns[0]["user"]
        return render_template("admin-select-runs.html",
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
        return render_template("admin-select-runs.html",
                                username=username,
                                title=session["title"],
                                pageLocation=json.dumps("userRun"),
                                selectedPoolNumber=selectedPoolNumber,
                                selectedUser=selectedUser,
                                selectedUserRun=selectedUserRun)
    userList = Helpers.getUserList(users)
    session["userList"] = userList
    return render_template("admin-select-runs.html",
                                username=username,
                                title=session["title"],
                                pageLocation=json.dumps("userForm"),
                                userList=userList)


@app.route("/admin-update-run", methods=["GET", "POST"])
def adminUpdateRun():
    """  Allows administrator to update runs for selected user """
    username = session["username"]
    selectedUser = session["selectedUser"]
    userRun = session["selectedUserRun"]
    existingPoolNumber = userRun[0]["pool"]
    existingChemistry = userRun[0]["chemistry"]
    existingExperiment = userRun[0]["experiment"]
    dropDownLists = Helpers.getDropDownLists(existingChemistry, existingExperiment)
    if request.method == "POST":
        updatedRun = Helpers.updateUserRun(runs, existingPoolNumber, selectedUser)
        userRun = [updatedRun["userRun"]]
        message = updatedRun["message"]
        if userRun[0] == "error":
            flash(message)
            userRun = session["userRun"]
            return render_template("update-user-run.html",
                                    username=username,
                                    title=session["title"],
                                    existingPoolNumber=existingPoolNumber,
                                    userRun=userRun,
                                    chemistryList=dropDownLists["chemistryList"], 
                                    experimentList=dropDownLists["experimentList"]) 
        else:
            flash(message)
            session["userRun"] = userRun
            newChemistry = userRun[0]["chemistry"]
            newExperiment = userRun[0]["experiment"]
            dropDownLists = Helpers.getDropDownLists(newChemistry, newExperiment)
            return render_template("update-user-run.html",
                                    username=username,
                                    title=session["title"],
                                    existingPoolNumber=existingPoolNumber,
                                    userRun=userRun,
                                    chemistryList=dropDownLists["chemistryList"], 
                                    experimentList=dropDownLists["experimentList"]) 
    return render_template("update-user-run.html",
                            username=username,
                            title=session["title"],
                            existingPoolNumber=existingPoolNumber,
                            userRun=userRun,
                            chemistryList=dropDownLists["chemistryList"], 
                            experimentList=dropDownLists["experimentList"]) 


@app.route("/admin-delete-run", methods=["GET", "POST"])
def adminDeleteRun():
    """  Delete selected run from database """
    username = session["username"]
    selectedPoolNumber = session["selectedPoolNumber"]
    if request.method == "POST":
        deletedRun = Helpers.deleteUserRun(runs, selectedPoolNumber)
        selectedUserRun = deletedRun["userRun"]
        if selectedUserRun == None:
            selectedUserRun = session["selectedUserRun"]
        message = deletedRun["message"]
        flash(message)
        pageLocation = deletedRun["pageLocation"]
        return render_template("admin-delete-run.html",
                                    username=username,
                                    title=session["title"],
                                    pageLocation=json.dumps(pageLocation),
                                    selectedUserRun=selectedUserRun)
    pageLocation =  "deleteRunForm"
    selectedUserRun = session["selectedUserRun"]
    return render_template("admin-delete-run.html",
                                username=username,
                                title=session["title"],
                                pageLocation=json.dumps(pageLocation),
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
            users = mongo.db.users
            users.remove({'user': selectedUserName})
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
    runData = Helpers.getRunData(runs, username)
    experimentData = Helpers.getExperimentData(runs, username)
    linechartData = Helpers.getLinechartData(runs, username)
    return render_template("user.html",
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
            return render_template("view-user-runs.html",
                                    username=username,
                                    title=session["title"],
                                    userRun=userRun,
                                    pageLocation=json.dumps("userRun"),
                                    userRunList=userRunList)
        elif request.form['formButton'] == 'userRuns':
            userRuns = Helpers.getUserRuns(runs, username)          
            Helpers.checkUserRuns(userRuns)
            return render_template("view-user-runs.html",
                                    username=username,
                                    title=session["title"],
                                    userRuns=userRuns,
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
    if request.method == "POST":
        message = Helpers.addUserRun(runs, username)
        flash(message)
        return redirect(url_for("addUserRun", username=username, title=session["title"]))
    return render_template("add-user-run.html", username=username, title=session["title"])


@app.route("/delete-user-run", methods=["GET", "POST"])
def deleteUserRun():
    """  Delete selected run from database """
    username = session["username"]
    poolNumber = session["poolNumber"]
    if request.method == "POST":
        deletedRun = Helpers.deleteUserRun(runs, poolNumber, username)
        userRun = deletedRun["userRun"]
        if userRun == None:
            userRun=session["userRun"]
        message = deletedRun["message"]
        flash(message)
        pageLocation = deletedRun["pageLocation"]
        return render_template("delete-user-run.html",
                                    username=username,
                                    title=session["title"],
                                    pageLocation=json.dumps(pageLocation),
                                    userRun=userRun)
    pageLocation =  "deleteRunForm"
    userRun=session["userRun"]
    return render_template("delete-user-run.html",
                                username=username,
                                title=session["title"],
                                pageLocation=json.dumps(pageLocation),
                                userRun=userRun)


@app.route("/update-user-run", methods=["GET", "POST"])
def updateUserRun():
    """  Update selected run from database """
    username = session["username"]
    userRun = session["userRun"]
    existingPoolNumber = userRun[0]["pool"]
    existingChemistry = userRun[0]["chemistry"]
    existingExperiment = userRun[0]["experiment"]
    dropDownLists = Helpers.getDropDownLists(existingChemistry, existingExperiment)
    if request.method == "POST":
        updatedRun = Helpers.updateUserRun(runs, existingPoolNumber, username)
        userRun = [updatedRun["userRun"]]
        message = updatedRun["message"]
        if userRun[0] == "error":
            flash(message)
            userRun = session["userRun"]
            return render_template("update-user-run.html",
                                    username=username,
                                    title=session["title"],
                                    existingPoolNumber=existingPoolNumber,
                                    userRun=userRun,
                                    chemistryList=dropDownLists["chemistryList"], 
                                    experimentList=dropDownLists["experimentList"]) 
        else:
            flash(message)
            session["userRun"] = userRun
            newChemistry = userRun[0]["chemistry"]
            newExperiment = userRun[0]["experiment"]
            dropDownLists = Helpers.getDropDownLists(newChemistry, newExperiment)
            return render_template("update-user-run.html",
                                    username=username,
                                    title=session["title"],
                                    existingPoolNumber=existingPoolNumber,
                                    userRun=userRun,
                                    chemistryList=dropDownLists["chemistryList"], 
                                    experimentList=dropDownLists["experimentList"]) 
    return render_template("update-user-run.html",
                            username=username,
                            title=session["title"],
                            existingPoolNumber=existingPoolNumber,
                            userRun=userRun,
                            chemistryList=dropDownLists["chemistryList"], 
                            experimentList=dropDownLists["experimentList"]) 


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)

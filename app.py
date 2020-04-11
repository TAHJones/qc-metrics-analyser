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
    session.clear()
    runData = Helpers.getRunData(runs)
    experimentData = Helpers.getExperimentData(runs)
    linechartData = Helpers.getLinechartData(runs)
    return render_template("pages/index.html",
                            runData=runData,
                            experimentData=experimentData,
                            linechartData=linechartData,
                            active="index",
                            loggedIn=False)


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log in with username. If username doesn't exist user is prompted to try another username.
    If user exists & has admin privileges they are directed to 'adminOrUser' page. Otherwise user is directed to 'user' page """
    session.clear()
    if request.method == "POST":
        session.clear()
        username = request.form.get("username")
        for user in users.find({}, {'user': 1, '_id': 0}):
            if user.get('user') == username:
                session["username"] = username
                member = users.find_one({'user': username}, { '_id': 0 }).get("member")
        if "username" in session and member == "admin":
            session["member"] = "admin"
            session["admin"] = True
            return redirect(url_for("adminOrUser", username=session["username"]))
        elif "username" in session and member == "user":    
            session["admin"] = False
            return redirect(url_for("user", username=session["username"]))
        else:
            flash("Username '{}' not found, please try a different username or sign up".format(username), "error")
            return render_template("pages/auth.html", active="login", loggedIn=False, loginFail=True)
    return render_template("pages/auth.html", active="login", loggedIn=False, loginFail=False)


@app.route("/logout/<username>")
def logout(username):
    """ log out user and return to homepage """
    if username != session["username"]:
        return redirect(url_for('permissionDenied'))
    else:
        return render_template('pages/logout.html',
                                username=username,
                                active="logout",
                                loggedIn=False)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """ Add new user to database. Check if username exists, if it does then user is prompted
    to try another username. If username doesn't exist add to database """
    session.clear()
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    if request.method == "POST":
        newUser = request.form.get('newUsername')
        for user in users.find({}, {'user': 1, '_id': 0}):
            if user.get('user') == newUser:
                flash("username {} already exists, enter a unique username or login".format(newUser), "error")
                return render_template("pages/auth.html", active="signup", loggedIn=False, loginFail=True)
        users.insert_one({'user':newUser, 'member':'user', 'joined':{'date':date, 'time':time}})
        flash("congratulations {}, your username has been added to the database".format(newUser), "success")
        return render_template("pages/auth.html", active="signup", loggedIn=False, loginFail=False)
    return render_template("pages/auth.html", active="signup", loggedIn=False, loginFail=False)


@app.route("/admin-or-user/<username>")
def adminOrUser(username):
    """ If user had admin rights give option to login as admin or user """
    # print(session["admin"])
    if username != session["username"]:
        return redirect(url_for('permissionDenied'))
    else:
        loggedIn = True
        if session["member"] == "admin":
            session["admin"] = True
        title = "WELCOME {}".format(username.upper())
        session["title"] = title
        return render_template("pages/admin-or-user.html",
                                title=title,
                                username=username,
                                active="adminOrUser",
                                loggedIn=loggedIn,
                                admin=session["admin"])


@app.route("/admin/login/<username>", methods=["GET", "POST"])
def adminLogin(username):
    """ admin page for removing & updating user & sequencing run data """
    if username != session["username"]:
        return redirect(url_for('permissionDenied'))
    else:
        loggedIn = True
        if session["member"] == "admin":
            session["admin"] = True
        if request.method == "POST":
            req = request.form
            email = req.get("email")
            for user in users.find({}, {'user': 1, 'email': 1, '_id': 0}):
                if user.get("user") == username and user.get("email") == email :
                    return redirect(url_for("admin",
                                    title=session["title"],
                                    username=username,
                                    active="admin",
                                    loggedIn=loggedIn,
                                    admin=session["admin"]))
            flash("email '{}' is incorrect, please enter correct address".format(email), "error")
            return redirect(url_for("adminLogin",
                                    title=session["title"],
                                    username=username,
                                    active="adminLogin",
                                    loggedIn=loggedIn,
                                    admin=session["admin"]))
        return render_template("/pages/auth.html",
                                title=session["title"],
                                username=username,
                                active="adminLogin",
                                loggedIn=loggedIn,
                                admin=session["admin"])


@app.route("/admin/<username>")
def admin(username):
    """ admin page for removing & updating user & sequencing run data """
    if username != session["username"]:
        return redirect(url_for('permissionDenied'))
    else:
        loggedIn = True
        return render_template("pages/admin.html",
        title=session["title"],
        username=username,
        active="admin",
        loggedIn=loggedIn,
        admin=session["admin"])


@app.route("/admin/select/runs/<username>", methods=["GET", "POST"])
def adminSelectRuns(username):
    """ select runs for individual users and then view, remove or update individual user runs """
    if username != session["username"]:
        return redirect(url_for('permissionDenied'))
    else:
        loggedIn = True
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
                                    userRuns=userRuns,
                                    active="adminSelectRuns",
                                    loggedIn=loggedIn,
                                    admin=session["admin"])
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
                                    selectedUserRun=selectedUserRun,
                                    active="adminSelectRuns",
                                    loggedIn=loggedIn,
                                    admin=session["admin"])
        userList = Helpers.getUserList(users)
        session["userList"] = userList
        return render_template("pages/admin-select-runs.html",
                                    username=username,
                                    title=session["title"],
                                    pageLocation=json.dumps("userForm"),
                                    userList=userList,
                                    active="adminSelectRuns",
                                    loggedIn=loggedIn,
                                    admin=session["admin"])


@app.route("/manage/runs/update/<username>", methods=["GET", "POST"])
def updateRun(username):
    """  Allows administrator to update runs for selected user """
    if username != session["username"]:
        return redirect(url_for('permissionDenied'))
    else:
        loggedIn = True
        if session["admin"] == True:
            userRun = session["selectedUserRun"]
        elif session["admin"] == False:
            userRun = session["userRun"]
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
            messageType = updatedRun["messageType"]
            if userRun[0] == "error":
                flash(message, messageType)
                userRun = session["userRun"]
                return render_template("pages/update-run.html",
                                        username=username,
                                        title=session["title"],
                                        existingPoolNumber=existingPoolNumber,
                                        userRun=userRun,
                                        chemistryList=dropDownLists["chemistryList"], 
                                        experimentList=dropDownLists["experimentList"],
                                        page="update-run",
                                        active="updateRun",
                                        loggedIn=loggedIn,
                                        admin=session["admin"])
            else:
                flash(message, messageType)
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
                                        active="updateRun",
                                        loggedIn=loggedIn,
                                        admin=session["admin"])
        return render_template("pages/update-run.html",
                                username=username,
                                title=session["title"],
                                existingPoolNumber=existingPoolNumber,
                                userRun=userRun,
                                chemistryList=dropDownLists["chemistryList"], 
                                experimentList=dropDownLists["experimentList"],
                                page="update-run",
                                active="updateRun",
                                loggedIn=loggedIn,
                                admin=session["admin"])


@app.route("/manage/runs/delete/<username>", methods=["GET", "POST"])
def deleteRun(username):
    """  Delete selected run from database """
    if username != session["username"]:
        return redirect(url_for('permissionDenied'))
    else:
        loggedIn = True
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
            messageType = deletedRun["messageType"]
            flash(message, messageType)
            pageLocation = deletedRun["pageLocation"]
            return render_template("pages/delete-run.html",
                                            username=username,
                                            title=session["title"],
                                            pageLocation=json.dumps(pageLocation),
                                            userRun=userRun,
                                            page = "delete-run",
                                            active="deleteRun",
                                            loggedIn=loggedIn,
                                            admin=session["admin"])
        pageLocation = "deleteRunForm"
        if session["admin"] == True:
            userRun = session["selectedUserRun"]
        else:
            userRun = session["userRun"]
        return render_template("pages/delete-run.html",
                                    username=username,
                                    title=session["title"],
                                    pageLocation=json.dumps(pageLocation),
                                    userRun=userRun,
                                    page = "delete-run",
                                    active="deleteRun",
                                    loggedIn=loggedIn,
                                    admin=session["admin"])


@app.route("/admin/select/user/<username>", methods=["GET", "POST"])
def adminSelectUser(username):
    """ select users to view, remove & update """
    if username != session["username"]:
        return redirect(url_for('permissionDenied'))
    else:
        loggedIn = True
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
                                        selectedUserName=selectedUserName,
                                        active="adminSelectUser",
                                        loggedIn=loggedIn,
                                        admin=session["admin"])
        userList = Helpers.getUserList(users)
        return render_template("pages/admin-select-user.html",
                                    username=username,
                                    title=session["title"],
                                    pageLocation=json.dumps("userForm"),
                                    userList=userList,
                                    active="adminSelectUser",
                                    loggedIn=loggedIn,
                                    admin=session["admin"])


@app.route("/admin/update/user/<username>", methods=["GET", "POST"])
def adminUpdateUser(username):
    """ select user to view, delete & update """
    if username != session["username"]:
        return redirect(url_for('permissionDenied'))
    else:
        loggedIn = True
        selectedUser = session["selectedUser"]
        selectedUserName = session["selectedUserName"]
        if request.method == "POST":
            updateUser = Helpers.adminUpdateUser(users, runs, selectedUserName)
            userData = updateUser["userData"]
            selectedUserName = userData["user"]
            message = updateUser["message"]
            messageType = updateUser["messageType"]
            flash(message, messageType)
            selectedUser = [userData]
            session["selectedUser"] = selectedUser
            session["selectedUserName"] = selectedUserName
            return render_template("pages/admin-update-user.html",
                                        username=username,
                                        title=session["title"],
                                        selectedUser=selectedUser,
                                        active="adminUpdateUser",
                                        loggedIn=loggedIn,
                                        admin=session["admin"])
        return render_template("pages/admin-update-user.html",
                                    username=username,
                                    title=session["title"],
                                    selectedUser=selectedUser,
                                    active="adminUpdateUser",
                                    loggedIn=loggedIn,
                                    admin=session["admin"])


@app.route("/admin/delete/user/<username>", methods=["GET", "POST"])
def adminDeleteUser(username):
    """ select user to view, delete & update """
    if username != session["username"]:
        return redirect(url_for('permissionDenied'))
    else:
        loggedIn = True
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
            messageType = deletedUser["messageType"]
            flash(message, messageType)
            pageLocation = deletedUser["pageLocation"]
            return render_template("pages/admin-delete-user.html",
                                        username=username,
                                        title=session["title"],
                                        pageLocation=json.dumps(pageLocation),
                                        selectedUser=selectedUser,
                                        selectedUserName=selectedUserName,
                                        active="adminDeleteUser",
                                        loggedIn=loggedIn,
                                        admin=session["admin"])
        return render_template("pages/admin-delete-user.html",
                                    username=username,
                                    title=session["title"],
                                    pageLocation=json.dumps("deleteUserForm"),
                                    selectedUser=selectedUser,
                                    selectedUserName=selectedUserName,
                                    active="adminDeleteUser",
                                    loggedIn=loggedIn,
                                    admin=session["admin"])


@app.route("/user/<username>")
def user(username):
    """ Display summary of run data for individual users """
    if username != session["username"]:
        return redirect(url_for('permissionDenied'))
    else:
        session["admin"] = False
        loggedIn = True
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
                                linechartData=linechartData,
                                active="user",
                                loggedIn=loggedIn,
                                admin=session["admin"])


@app.route("/user/view/runs/<username>", methods=["GET", "POST"])
def viewUserRuns(username):
    """  view all user runs or select individual run to delete or update """
    if username != session["username"]:
        return redirect(url_for('permissionDenied'))
    else:
        loggedIn = True
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
                                        userRunList=userRunList,
                                        active="viewUserRuns",
                                        loggedIn=loggedIn,
                                        admin=session["admin"])
            elif request.form['formButton'] == 'userRuns':
                userRuns = Helpers.getUserRuns(runs, username)          
                Helpers.checkUserRuns(userRuns)
                return render_template("pages/view-user-runs.html",
                                        username=username,
                                        title=session["title"],
                                        userRuns=userRuns,
                                        pageLocation=json.dumps("userRuns"),
                                        userRunList=userRunList,
                                        active="viewUserRuns",
                                        loggedIn=loggedIn,
                                        admin=session["admin"])                          
        return render_template("pages/view-user-runs.html",
                                username=username,
                                title=session["title"],
                                pageLocation=json.dumps("userForm"),
                                userRunList=userRunList,
                                active="viewUserRuns",
                                loggedIn=loggedIn,
                                admin=session["admin"])


@app.route("/user/add/run/<username>", methods=["GET", "POST"])
def addUserRun(username):
    """  Add new run to database """
    if username != session["username"]:
        return redirect(url_for('permissionDenied'))
    else:
        loggedIn = True
        username = session["username"]
        if request.method == "POST":
            addUserMessage = Helpers.addUserRun(runs, username)
            message = addUserMessage["messageInfo"]
            messageType = addUserMessage["messageType"]
            flash(message, messageType)
            return redirect(url_for("addUserRun", username=username, title=session["title"]))
        return render_template("pages/add-user-run.html",
                                username=username,
                                title=session["title"],
                                active="addUserRun",
                                loggedIn=loggedIn,
                                admin=session["admin"])


@app.route("/permission-denied")
def permissionDenied():
    """ Displayed if username url var doesn't match session username var """
    return render_template("pages/permission-denied.html", active="errorPage", loggedIn=False)


@app.errorhandler(404) 
def pageNotFound(e): 
    """ Displays custom 404 page if url isn't recognised """ 
    return render_template("pages/404.html", active="errorPage", loggedIn=False) 


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)

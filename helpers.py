from flask import request, flash


class Helpers:
    """ Gets the number of each catergory for 'experiment' or 'chemistry' data types.
    'Experiment' catergories are 'Genome', 'Exome' or 'Capture'.
    'Chemistry' catergories are 'Mid300', 'Mid150' or 'High300'. """
    @staticmethod
    def getDataCount(database, dataType, dataCatergory, user="N/A"):
        singleUser = {'$match': {dataType: dataCatergory}}
        allUsers = {'$match': {'$and': [{'user': user}, {dataType: dataCatergory}]}}
        dataCount = {'$group': { '_id': 'null','count': {'$sum': 1},}}
        if user == "N/A":
            databaseQuery = [singleUser, dataCount]
        else:
            databaseQuery = [allUsers, dataCount]
        dataCount = list(database.aggregate(databaseQuery))
        return dataCount


    """ Gets the min, max & average values for data that matchs the parameter 'param'.
    'param' parameter can be 'yields', 'clusterDensity', 'passFilter' or 'q30'. """
    @staticmethod
    def getDataSummary(database, param, user="N/A"):
        dollarParam = "${}".format(param)
        allUsers = {'$match': {'user': {'$exists': 'true'}}}
        singleUser = {'$match': {'user': user}}
        dataSummary = {
                '$group': {
                '_id': 'null',
                'count': { '$sum': 1 },
                'average': {'$avg': dollarParam},
                'minimum': {'$min': dollarParam},
                'maximum': {'$max': dollarParam}
            }
        }
        if user == "N/A":
            databaseQuery = [allUsers, dataSummary]
        else:
            databaseQuery = [singleUser, dataSummary]   
        myresult = list(database.aggregate(databaseQuery))
        if myresult == []:
            myresult = [{'_id': 'null', 'count': 0, 'average': 0, 'minimum': 0, 'maximum': 0}]
        return myresult


    """ Take nested list of experiment types & catergory names & uses 
    a nested loop to feed them into getDataCount function. """
    @staticmethod
    def getExperimentData(database, user="N/A"):
        experiments = {"chemistry": ["Mid300", "Mid150", "High300"], "experiment": ["Genome", "Exome", "Capture"]}
        experimentData = {}
        for experiment in experiments:
            catergoryDicts = {}
            for catergoryName in experiments[experiment]:
                if user == "N/A":
                    catergoryValue = Helpers.getDataCount(database, experiment, catergoryName)
                    if catergoryValue == []:
                        catergoryValue = [{'_id': 'null', 'count': 0}]
                else:
                    catergoryValue = Helpers.getDataCount(database, experiment, catergoryName, user)
                    if catergoryValue == []:
                        catergoryValue = [{'_id': 'null', 'count': 0}]
                catergoryDict = {catergoryName.lower():catergoryValue[0]["count"]}
                catergoryDicts.update(catergoryDict)
            experimentData[experiment] = catergoryDicts
        return experimentData


    """ Take list of qc metrics & feeds them into getDataSummary function. """
    @staticmethod
    def getRunData(database, user="N/A"):
        metrics = ("yield", "clusterDensity", "passFilter", "q30")
        metricsData = {}
        for metric in metrics:
            if user == "N/A":
                metricValue = Helpers.getDataSummary(database, metric)
            else:
                metricValue = Helpers.getDataSummary(database, metric, user)
            if metric == "yield":
                metric = "yields"
            metricsDict = { metric: {"minimum":metricValue[0]["minimum"], "maximum":metricValue[0]["maximum"], "average":metricValue[0]["average"]} }
            metricsData.update(metricsDict)
        return metricsData


    """ Takes dict object from getExperimentData & getRunData functions, 
    joins them together then adds them to qcData dict. """
    @staticmethod
    def getQCData(database, user="N/A"):
        qcData = {}
        if user == "N/A":
            experimentData = Helpers.getExperimentData(database)
            runData = Helpers.getRunData(database)
        else:
            experimentData = Helpers.getExperimentData(database, user)
            runData = Helpers.getRunData(database, user)
        experimentData.update(runData)
        qcData = experimentData
        return qcData


    """ Mongodb query that gets qc metric data for 
    all user runs or all runs for a selected user. """
    @staticmethod
    def getLinechartData(database, user="N/A"):
        if user == "N/A":
            dbChartData = list(database.find({}, { 'pool': 1, 'yield': 1, 'passFilter': 1, 'clusterDensity': 1, 'q30': 1, '_id': 0 }))
        else:
            dbChartData = list(database.find({ 'user': user }, { 'pool': 1, 'yield': 1, 'passFilter': 1, 'clusterDensity': 1, 'q30': 1, '_id': 0 }))

        pools = []
        yields = []
        clusterDensity = []
        passFilter = []
        q30 = []

        for data in dbChartData:
            pools.append(data["pool"])
            yields.append(data["yield"])
            clusterDensity.append(data["clusterDensity"])
            passFilter.append(data["passFilter"])
            q30.append(data["q30"])
        
        linechartData = {
            "pools": pools,
            "yields": yields,
            "clusterDensity": clusterDensity,
            "passFilter": passFilter,
            "q30": q30
        }
        return linechartData


    """ Gets list of all runs from all users.
    Takes database collection name as parameter  """
    @staticmethod
    def getRunList(database):
        runList = list(database.find({}, { 'pool': 1, '_id': 0 }))
        return runList


    """ Gets list of all runs for an individual user.
    Takes database collection name & username as parameters  """
    @staticmethod
    def getUserRunList(database, user):
        userRunList = list(database.find({ 'user': user }, { 'pool': 1, '_id': 0 }))
        return userRunList


    """ Gets list of all users from database users collection.
    Takes database collection name as parameter  """
    @staticmethod
    def getUserList(database):
        userList = list(database.find({}, {'user': 1, '_id': 0}))
        return userList


    """ Gets form data from post request & returns data as formData dict"""
    @staticmethod
    def getFormData(*intArgs):
        formData = {}
        missing = list()
        req = request.form
        for k, v in req.items():
            if v == "":
                missing.append(k)
            if k in intArgs:
                formData[k] = int(v)
            else:
                formData[k] = v
        if missing:
            flash(f"Missing fields for {', '.join(missing)}", "error")
        return formData


    """ Gets form data from post request & return data as formData dict. """
    @staticmethod
    def getRunFormData(*strArgs):
        formData = {}
        missing = list()
        req = request.form
        for k, v in req.items():
            if v == "":
                missing.append(k)
            if k in strArgs:
                formData[k] = v
            else:
                formData[k] = int(v)
        if missing:
            flash(f"Missing fields for {', '.join(missing)}", "error")
        return formData


    """ Takes data from formData function & generates 
    database query to fetch data for individual user run """
    @staticmethod
    def getUserRun(database, user="N/A"):
        formData = Helpers.getFormData("poolNumber")
        if user == "N/A":
            userQuery = formData["username"]
        else:
            userQuery = user
        poolNumber = formData["poolNumber"]
        dbQuery = {'user': userQuery, 'pool': poolNumber}
        userRun = list(database.find(dbQuery, { '_id': 0 }))
        return userRun


    """ Takes data from getRunFormData function & generates database 
    query to get data for a selection or all runs for active user.
    Takes database collection name & username as parameters """
    @staticmethod
    def getUserRuns(database, user="N/A"):
        formData = Helpers.getRunFormData("username", "formButton", "chemistry", "experiment")
        if user == "N/A":
            userQuery = {'user': formData["username"]}
        else:
            userQuery = {'user': user}
        chemistry = formData["chemistry"]
        experiment = formData["experiment"]
        yieldsQuery = {'$and': [{'yield': {'$gte': formData["minYield"]}}, {'yield': {'$lte': formData["maxYield"]}}]}
        clusterDensityQuery = {'$and': [{'clusterDensity': {'$gte': formData["minClusterDensity"]}}, {'clusterDensity': {'$lte': formData["maxClusterDensity"]}}]}
        passFilterQuery = {'$and': [{'passFilter': {'$gte': formData["minPassFilter"]}}, {'passFilter': {'$lte': formData["maxPassFilter"]}}]}
        q30Query = {'$and': [{'q30': {'$gte': formData["minq30"]}}, {'q30': {'$lte': formData["maxq30"]}}]}
        chemistryQuery = {'chemistry': chemistry}
        experimentQuery = {'experiment': experiment}

        if chemistry == "All" and experiment == "All":
            dbQuery = {'$and': [userQuery, yieldsQuery, clusterDensityQuery, passFilterQuery, q30Query]}
        elif chemistry != "All" and experiment == "All":
            dbQuery = {'$and': [userQuery, yieldsQuery, clusterDensityQuery, passFilterQuery, q30Query, chemistryQuery]}
        elif chemistry == "All" and experiment != "All":
            dbQuery = {'$and': [userQuery, yieldsQuery, clusterDensityQuery, passFilterQuery, q30Query, experimentQuery]}
        elif chemistry != "All" and experiment != "All":
            dbQuery = {'$and': [userQuery, yieldsQuery, clusterDensityQuery, passFilterQuery, q30Query, chemistryQuery, experimentQuery]}

        userRuns = list(database.find(dbQuery, { '_id': 0 }))
        return userRuns


    """ Checks qc metric values are within accepted range when a new run is added.
    Checks each qc metric value in turn & returns a message for the 1st value outside of range.
    If all values are within accepted range then the message 'pass' is returned
    Takes data from 'add user run' form as a parameter  """
    @staticmethod
    def checkMetricValues(data):
        if "yield" in data:
            yields = data["yield"]
        elif "yields" in data:
            yields = data["yields"]
        clusterDensity = data["clusterDensity"]
        passFilter = data["passFilter"]
        q30 = data["q30"]
        if yields < 1 or yields > 250:
            message = "Yield should be between 1 and 250, but is {}".format(yields)
            return message
        elif clusterDensity < 50 or clusterDensity > 250:
            message = "Cluster density should be between 50 and 250, but is {}".format(clusterDensity)
            return message
        elif passFilter < 1 or passFilter > 100:
            message = "Pass filter should be between 1 and 100, but is {}".format(passFilter)
            return message
        elif q30 < 1 or q30 > 100:
            message = "Q30 should be between 1 and 100, but is {}".format(q30)
            return message
        else:
            message = "pass"
            return message


    """ Gets form data for new user run & checks data is correct with help of getRunList & checkMetricValues functions.
    If data is incorrect returns message var which is passed to flash message function.
    If data is correct adds new run to database and returns message var which is passed to flash message function.
    Takes database collection name & username as parameters """
    @staticmethod
    def addUserRun(database, user):
        addUserMessage = {}
        runList = Helpers.getRunList(database)
        formData = Helpers.getRunFormData("user", "chemistry", "experiment", "comment")
        message = Helpers.checkMetricValues(formData)
        poolNumber = formData["pool"]
        formName = formData["user"]
        if user != formName:
            addUserMessage["messageInfo"] = "Username '{}' is incorrect".format(formName)
            addUserMessage["messageType"] = "error"
            return message
        elif user == formName:
            for run in runList:
                if run["pool"] == poolNumber:
                    addUserMessage["messageInfo"] = "Pool_{} already exists, enter a unique number".format(poolNumber)
                    addUserMessage["messageType"] = "error"
                    return message
            if message == "pass":
                database.insert_one(formData)
                addUserMessage["messageInfo"] = "Pool_{} has been successfully added".format(poolNumber)
                addUserMessage["messageType"] = "success"
        return addUserMessage


    """ Checks if database query returns empty list. If true it replaces empty 
    list with list containing key:value pairs where all values are zero.
    Takes results of database query as a function parameter """
    @staticmethod
    def checkUserRuns(runs):
        if runs == []:
            flash('No runs of that type were found', 'error')
            runs = [{'run': 0,'pool': 0,'yield': 0,'clusterDensity': 0,'passFilter': 0,'q30': 0}]
        return runs


    """ Generates list of dropdown options from update run form.
    dataList parameter is either list of chemistry or experiment catergories.
    currentSelection parameter is the currently selected catergory item 
    & is made dropdown list default value. """
    @staticmethod
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


    """ Generates dropdown lists for chemistry & experiment catergories.
    Uses createDropDownList function to create lists & adds to dropDownLists dict.
    Takes currently selected chemistry & experiment catergories as parameters  """
    @staticmethod
    def getDropDownLists(selectedChemistry, selectedExperiment):
        dropDownLists = {}
        chemistryTypes = ["High300", "Mid300", "Mid150"]
        experimentTypes = ["Genome", "Exome", "Capture"]
        dropDownLists["chemistryList"] = Helpers.createDropDownList(chemistryTypes, selectedChemistry)
        dropDownLists["experimentList"] = Helpers.createDropDownList(experimentTypes, selectedExperiment)
        return dropDownLists


    """  Takes checkbox form data & if value is 'yes' it deletes selected run from database
    It returns dict of qc metrics key:values pairs where values is 'Deleted', pageLocation & message var
    Takes database collection name, pool number & optional username as parameters """
    @staticmethod
    def deleteUserRun(database, poolNumber, user="N/A"):
        deletedRun = {}
        radio = request.form.get("radio")
        if radio == 'yes':
            deletedRun["userRun"] = [{
                'pool': 'Deleted',
                'yield': 'Deleted',
                'clusterDensity': 'Deleted',
                'passFilter': 'Deleted',
                'q30': 'Deleted',
                'experiment': 'Deleted',
                'chemistry': 'Deleted'
            }]
            if user == "N/A":
                database.remove({'pool': poolNumber})
            else:
                database.remove({'user': user, 'pool': poolNumber})
            deletedRun["pageLocation"] = "runDeleted"
            deletedRun["message"] = "Pool_{} has been successfully deleted".format(poolNumber)
            deletedRun["messageType"] = "success"
        elif radio == 'no':
            deletedRun["userRun"] = None
            deletedRun["pageLocation"] = "deleteRunForm"
            deletedRun["message"] = "To delete Pool_{} select 'Yes' then click 'Delete'".format(poolNumber)
            deletedRun["messageType"] = "error"
        return deletedRun


    """ Gets updated form data & validates it. If incorrect an error message is returned. 
    If all data is correct it adds updated run to database & returns form data as dict.
    Takes database collection name, pool number & optional username as parameters """
    @staticmethod
    def updateUserRun(database, run, user):
        updatedRun = {}
        poolList = Helpers.getRunList(database)
        formData = Helpers.getRunFormData("user", "chemistry", "experiment", "comment", "formName")
        message = Helpers.checkMetricValues(formData)
        formName = formData["user"]
        poolNumber = formData["pool"]
        if user != formName:
            message = "Username '{}' is incorrect".format(formName)
        elif user == formName:
            for pool in range(len(poolList)): 
                if poolList[pool]['pool'] == run: 
                    del poolList[pool] 
                    break
            for pool in poolList:
                if pool["pool"] == poolNumber:
                    message = "Pool_{} already exists, enter a unique number".format(poolNumber)
        if message != "pass":
            updatedRun["message"] = message
            updatedRun["userRun"] = "error"
            updatedRun["messageType"] = "error"
        else:
            database.update_one({'user': user, 'pool': run}, {'$set': formData})
            message = "Pool_{} has been successfully updated".format(run)
            updatedRun["userRun"] = formData
            updatedRun["message"] = message
            updatedRun["messageType"] = "success"
        return updatedRun


    """ Takes data from getFormData function & generates 
    database query to get user data for selected user.
    Takes database collection name as parameters """
    @staticmethod
    def adminSelectUser(database):
        formData = Helpers.getFormData()
        selectedUser = list(database.find({'user': formData["user"]}, { '_id': 0 }))
        return selectedUser


    """ Gets updated user form data, generates database queries 
    to update selected user & users runs then returns form data as dict.
    Takes database user & runs collection names & username as parameters """
    @staticmethod
    def adminUpdateUser(userDatabase, runDatabase, user):
        updateUser = {}
        formData = Helpers.getFormData()
        userData = {
            'user': formData["user"],
            'member': formData["member"],
            'joined': {'date': formData["date"], 'time': formData["time"]}
        }
        userDatabase.update_one({'user': user}, {'$set': userData})
        runDatabase.update_many({'user': user}, {'$set': {'user': formData["user"]}})
        updateUser["message"] = "User account for {} has been successfully updated".format(user)
        updateUser["messageType"] = "success"
        updateUser["userData"] = userData
        return updateUser


    """  Takes checkbox form data & if value is 'yes' it deletes selected user & slected users runs from database
    It returns dict of user data key:values pairs where values is 'Deleted', pageLocation & message var
    Takes database user & runs collection names & username as parameters """
    @staticmethod
    def adminDeleteUser(userDatabase, runDatabase, user):
        deletedUser = {}
        radio = request.form.get("radio")
        if radio == 'yes':
            userData = {
                'user': 'Deleted',
                'member': 'Deleted',
                'joined': {'date': 'Deleted', 'time': 'Deleted'}
            }
            deletedUser["userData"] = userData
            deletedUser["pageLocation"] = "userDeleted"
            deletedUser["message"] = "User account for {} has been successfully deleted".format(user)
            deletedUser["messageType"] = "success"
            userDatabase.remove({'user': user})
            runDatabase.remove({'user': user})
        elif radio == 'no':
            deletedUser["userData"] = None
            deletedUser["pageLocation"] = "deleteUserForm"
            deletedUser["message"] = "To delete user account for {} select 'Yes' then click 'Delete'".format(user)
            deletedUser["messageType"] = "error"
        return deletedUser

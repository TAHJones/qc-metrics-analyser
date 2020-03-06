from flask import request, flash, session


class Helpers:
    """ Mongodb query that counts the number incidences of each catergory for a given data type for a selected user or for all users if no user parameter is given.
    Data types can either be 'experiment' or 'chemistry'. 
    For the data type 'experiment' catergories are 'Genome', 'Exome' or 'Capture'.
    For the data type 'chemistry' catergories are 'Mid300', 'Mid150' or 'High300'. """
    @staticmethod
    def getDataCount(database, dataType, dataCatergory, user="N/A"):
        if user == "N/A":
            databaseQuery = [
                {
                    '$match': {
                        dataType: dataCatergory
                    }
                },
                {
                    '$group': {
                        '_id': 'null',
                        'count': { '$sum': 1 },
                    }
                }
            ]
        else:
            databaseQuery = [
            {
                '$match': {
                    '$and': [ {'user': user}, {dataType: dataCatergory} ]
                }
            },
            {
                '$group': {
                    '_id': 'null',
                    'count': { '$sum': 1 },
                }
            }
            ]
        dataCount = list(database.aggregate(databaseQuery))
        return dataCount


    """ Mongodb query that gets the min, max & average values for data that matchs the parameter 'param'.
    The query can be for a selected user or for all users if no user parameter is given.
    'param' parameter should be 'yields', 'clusterDensity', 'passFilter' or 'q30'. """
    @staticmethod
    def getDataSummary(database, param, user="N/A"):
        dollarParam = "${}".format(param)
        if user == "N/A":
            databaseQuery = [
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
            }]
        else:
            databaseQuery = [
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
            }]
        return list(database.aggregate(databaseQuery))


    """ Take nested list of experiment types & catergory names & uses a nested loop to feed them into getDataCount function.
    Takes the mongodb connect string as a parameter & user as an optional parameter which are passed to the getDataCount function.
    Returns a dict object containing the number for each catergory for each experiment type """
    @staticmethod
    def getExperimentData(database, user="N/A"):
        experiments = {"experiment": ("Genome", "Exome", "Capture"), "chemistry": ("Mid300", "Mid150", "High300")}
        experimentData = {}
        for experiment in experiments:
            for catergory in experiments[experiment]:
                if user == "N/A":
                    catergoryValue = Helpers.getDataCount(database, experiment, catergory)
                    if catergoryValue == []:
                        catergoryValue = [{'_id': 'null', 'count': 0}]
                else:
                    catergoryValue = Helpers.getDataCount(database, experiment, catergory, user)
                    if catergoryValue == []:
                        catergoryValue = [{'_id': 'null', 'count': 0}]
                catergoryDict = {catergory.lower():catergoryValue[0]["count"]}
                experimentData.update(catergoryDict)
        return experimentData


    """ Take dict list of qc metrics types & uses a loop to feed them into getDataSummary function.
    Takes the mongodb connect string as a parameter & user as an optional parameter which are passed to the getDataSummary function.
    Returns a dict object containing the min, max & avg values for each qc metrics type """
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


    """ Takes dict object from getExperimentData & getRunData functions, joins them together then adds them to qcData dict.
    Takes the mongodb connect string as a parameter & user as an optional parameter which are passed to the getExperimentData & getRunData functions.
    Returns a dict object containing all the qc data generated by the getExperimentData & getRunData functions. """
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

    """ Gets form data from post request & adds to req var.
    Loops through req adding each key:value pair to formData dict.
    Checks if values are missing & sends list of missing values to flash message.
    Checks optional parameters 'intArgs' against values from form, 
    matching values are converted to integers, all other form values remain as strings """
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
            flash(f"Missing fields for {', '.join(missing)}")
        return formData


    """ Gets form data from post request & adds to req var.
    Loops through req adding each key:value pair to formData dict.
    Checks if values are missing & sends list of missing values to flash message.
    Checks optional parameters 'strArgs' against values from form, 
    matching values remain as strings, all other form values are converted to integers """
    @staticmethod
    def getFilteredFormData(*strArgs):
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
            flash(f"Missing fields for {', '.join(missing)}")
        return formData


    @staticmethod
    def getUserRun(database, user="N/A"):
        formData = Helpers.getFormData("selectedPoolNumber")
        if user == "N/A":
            userQuery = formData["username"]
        else:
            userQuery = user
        selectedPoolNumber = formData["selectedPoolNumber"]
        dbQuery = {'user': userQuery, 'pool': selectedPoolNumber}
        userRun = list(database.find(dbQuery, { '_id': 0 }))
        return userRun


    @staticmethod
    def getUserRuns(database, user="N/A"):
        formData = Helpers.getFilteredFormData("username", "formButton", "chemistry", "experiment")
        if user == "N/A":
            userQuery = {'user': formData["username"]}
        else:
            userQuery = {'user': user}
        chemistry = formData["chemistry"]
        experiment = formData["experiment"]
        yieldsQuery = {'$and': [{'yield': {'$gt': formData["minYield"]}}, {'yield': {'$lt': formData["maxYield"]}}]}
        clusterDensityQuery = {'$and': [{'clusterDensity': {'$gt': formData["minClusterDensity"]}}, {'clusterDensity': {'$lt': formData["maxClusterDensity"]}}]}
        passFilterQuery = {'$and': [{'passFilter': {'$gt': formData["minPassFilter"]}}, {'passFilter': {'$lt': formData["maxPassFilter"]}}]}
        q30Query = {'$and': [{'q30': {'$gt': formData["minq30"]}}, {'q30': {'$lt': formData["maxq30"]}}]}
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
        if userRuns == []:
            flash('No Runs of that type were found')
            userRuns = [{'run': 0,'pool': 0,'yield': 0,'clusterDensity': 0,'passFilter': 0,'q30': 0}]
        elif userRuns != [] and user == "N/A":
            session["selectedUser"] = formData["username"]
        return userRuns

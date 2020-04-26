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
    query to get data for a selection or all runs for active user. """
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


    """ Checks qc metric values are within accepted range when a new run is added. """
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


    """ Gets form data for new user run, checks data then 
    adds new run to database and returns message var. """
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
            return addUserMessage
        elif user == formName:
            for run in runList:
                if run["pool"] == poolNumber:
                    addUserMessage["messageInfo"] = "Pool_{} already exists, enter a unique number".format(poolNumber)
                    addUserMessage["messageType"] = "error"
                    return addUserMessage
        if message == "pass":
            database.insert_one(formData)
            addUserMessage["messageInfo"] = "Pool_{} has been successfully added".format(poolNumber)
            addUserMessage["messageType"] = "success"
        elif message != "pass":
            addUserMessage["messageInfo"] = message
            addUserMessage["messageType"] = "error"
        return addUserMessage


    """ Checks if database query returns empty list. If true it replaces empty 
    list with list containing key:value pairs where all values are zero. """
    @staticmethod
    def checkUserRuns(runs):
        if runs == []:
            flash('No runs of that type were found', 'error')
            runs = [{'run': 0,'pool': 0,'yield': 0,'clusterDensity': 0,'passFilter': 0,'q30': 0}]
        return runs


    """ Generates list of dropdown options from update run form. """
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


    """ Generates dropdown lists for chemistry & experiment catergories. """
    @staticmethod
    def getDropDownLists(selectedChemistry, selectedExperiment):
        dropDownLists = {}
        chemistryTypes = ["High300", "Mid300", "Mid150"]
        experimentTypes = ["Genome", "Exome", "Capture"]
        dropDownLists["chemistryList"] = Helpers.createDropDownList(chemistryTypes, selectedChemistry)
        dropDownLists["experimentList"] = Helpers.createDropDownList(experimentTypes, selectedExperiment)
        return dropDownLists


    """  Takes checkbox form data & if value is 
    'yes' it deletes selected run from database """
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


    """ Gets updated form data, validates it, then adds 
    updated run to database & returns form data as dict. """
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
    database query to fetch user data for selected user. """
    @staticmethod
    def adminSelectUser(database):
        formData = Helpers.getFormData()
        selectedUser = list(database.find({'user': formData["user"]}, { '_id': 0 }))
        return selectedUser


    """ Gets updated user form data, generates database queries 
    to update selected user & users runs then returns form data as dict. """
    @staticmethod
    def adminUpdateUser(userDatabase, runDatabase, user):
        updateUser = {}
        formData = Helpers.getFormData()
        userData = {
            'user': formData["user"],
            'member': formData["member"],
            'joined': {'date': formData["date"], 'time': formData["time"]},
            'email': formData["email"]
        }
        userDatabase.update_one({'user': user}, {'$set': userData})
        runDatabase.update_many({'user': user}, {'$set': {'user': formData["user"]}})
        updateUser["message"] = "User account for {} has been successfully updated".format(user)
        updateUser["messageType"] = "success"
        updateUser["userData"] = userData
        return updateUser


    """  Takes checkbox form data & if value is 'yes' it deletes 
    selected user account & selected users runs from database """
    @staticmethod
    def adminDeleteUser(userDatabase, runDatabase, user):
        deletedUser = {}
        radio = request.form.get("radio")
        if radio == 'yes':
            userData = {
                'user': 'Deleted',
                'member': 'Deleted',
                'joined': {'date': 'Deleted', 'time': 'Deleted'},
                'email': 'Deleted'
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


    """ Returns information about each sequencing qc metric 
    which is used by popup button in linechart modal """
    @staticmethod
    def getMetricInfo():
        metricInfo = {}
        metricData = {
            'intro': {
                'title': 'Next Generation Sequencing',
                'info': 'Next Generation Sequencing (NGS) is a high-throughput DNA sequencing technology used to sequence all or a portion of the DNA of an organism\'s genome at a single time. This is possible because NGS technologies are capable of processing multiple DNA sequences in parallel, generating millions of sequencing reads in a single experiment. This is why NGS is also called massively parallel sequencing. Illuminas NGS technology, called sequencing by synthesis, is a widely adopted sequencing technology. This approach records the incorporation of fluorescently labeled nucleotides, into clonally amplified DNA templates immobilized to an acrylamide coating on the surface of a glass flowcell. Essentially the DNA molecules are sequenced as they are being synthesized.',
                'link': 'https://emea.illumina.com/science/technology/next-generation-sequencing/sequencing-technology.html?langsel=/gb/'
            },
            'yield': {
                'title': 'Yield - GB',
                'info': 'This shows the projected number of bases called for the run, measured in mega-bases. This figure is an estimation of the amount of sequencing data produced during the run but gives no indication of the quality of the data.',
                'link': 'https://support.illumina.com/help/BaseSpace_Sequence_Hub/Source/Informatics/BS/Yield_swBS.htm'
            },
            'clusterDensity': {
                'title': 'Cluster Density - K/mm2',
                'info': 'Cluster density is an important metric that influences run quality, reads passing filter, Q30 scores, and total data output. While under-clustering maintains high data quality, it results in lower data output. Alternatively, over-clustering can lead to poor run performance, lower Q30 scores and lower total data output (decrease in the pass-filter metric).',
                'link': 'https://emea.illumina.com/content/dam/illumina-marketing/documents/products/other/miseq-overclustering-primer-770-2014-038.pdf'
            },
            'passFilter': {
                'title': 'Pass Filter - %',
                'info': 'The percentage of clusters passing filter is an indication of signal purity from each cluster. Over clustering (high cluster density) typically generates a larger number of overlapping clusters. This leads to poor template generation, which causes a decrease in the pass-filter metric. Decreased cluster intensity also has a limited effect on sequencing quality but will obviously affect yield and therefore sequencing coverage.',
                'link': 'https://gatk.broadinstitute.org/hc/en-us/articles/360035890991-PF-reads-Illumina-chastity-filter'
            },
            'q30': {
                'title': 'Q30 Score - %',
                'info': 'This shows the average percentage of bases greater than Q30. A quality score (Q-score) is a prediction of the probability of an error in base calling. For base calls with a quality score of Q30, one base call in 1,000 is predicted to be incorrect. Q30 quality scores are used across all Illumina sequencing platforms. When sequencing quality reaches Q30, virtually all of the reads will be correct. This is why Q30 is considered the bench mark for quality for next generation sequencing data.',
                'link': 'https://emea.illumina.com/documents/products/technotes/technote_Q-Scores.pdf'
            },
            'experiment': {
                'title': 'Experiment',
                'info': 'Genomic sequencing also known as whole genome sequencing is the process of sequencing all the DNA of an organism\'s genome at a single time. This includes all of an organism\'s chromosomal DNA, including all the non-coding as well as coding regions. Exome experiments sequencing, also known as whole exome sequencing, is the process of sequencing all of the coding regions of genes (exons) of in an organisms genome. Capture based sequencing also known as target enrichment is the process of sequencing a subset of genes or regions of the genome. Target enrichment works by capturing genomic regions of interest by hybridization to target-specific biotinylated probes, which are then isolated by magnetic pulldown.',
                'link': 'https://en.wikipedia.org/wiki/Whole_genome_sequencing'
            },
            'chemistry': {
                'title': 'Chemistry',
                'info': 'High300 generates 100–120 Gb sequencing data. Mid300 generates 32.5–39 Gb sequencing data. Mid150 generates 16.25–19.5 Gb sequencing data.',
                'link': 'https://emea.illumina.com/systems/sequencing-platforms/nextseq/specifications.html'
            }
        }

        for key, value in metricData.items():
            metricInfo[key] = '<div class="popup-info">' + value['info'] + '</div><div class="popup-link"><a class="btn btn-lg btn-info" href="' + value['link'] + '" target="_blank">' + 'More Info' + '</a></div>'

        return metricInfo
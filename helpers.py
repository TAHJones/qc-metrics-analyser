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


    @staticmethod
    def getExperimentData2(database, user="N/A"):
        experiments = {"experiment": ("Genome", "Exome", "Capture"), "chemistry": ("Mid300", "Mid150", "High300")}
        experimentsData = {}
        for experiment in experiments:
            experimentData = {}
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
            experimentData[experiment] += catergoryDict
        experimentsData += experimentData
        return experimentsData


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
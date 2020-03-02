import os
# from os import path
# if path.exists("env.py"):
#     import env
from flask import Flask, render_template, redirect, request, url_for, flash, session, json
from flask_pymongo import PyMongo
# from datetime import datetime
# from helpers import Helpers

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
        if databaseQuery == []:
            databaseQuery = [{'count': 0}]
        return list(database.aggregate(databaseQuery))


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
        return database.aggregate(databaseQuery)

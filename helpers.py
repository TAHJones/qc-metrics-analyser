import os
# from os import path
# if path.exists("env.py"):
#     import env
from flask import Flask, render_template, redirect, request, url_for, flash, session, json
from flask_pymongo import PyMongo
# from datetime import datetime
# from helpers import Helpers

class Helpers:
    """ Mongodb query that counts the number of experiments for all users that match the parameter 'experiment'.
    Experiment parameter should be 'Genome', 'Exome' or 'Capture'. """
    @staticmethod
    def getDataCount(database, dataType, dataCatergory, user="N/A"):
        if user == "N/A":
            data = list(database.aggregate([
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
            ]))
        else:
            data = list(database.aggregate([
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
            ]))
            if data == []:
                data = [{'count': 0}]
        return data


    """ Mongodb query that counts the number of experiments for all users that match the parameter 'experiment'.
    Experiment parameter should be 'Genome', 'Exome' or 'Capture'. """
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

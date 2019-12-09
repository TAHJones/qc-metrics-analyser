import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'sequencingMetricsDB'
app.config["MONGO_URI"] = 'mongodb+srv://seqMetRoot:seqMetR00tUser@sequencingmetricsdb-kpu2s.mongodb.net/sequencingMetricsDB?retryWrites=true&w=majority'


mongo = PyMongo(app)

@app.route("/")
@app.route("/get_metrics")
def getMetrics():
    return render_template("get-metrics.html", metrics=mongo.db.seqMetCol.find())


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)

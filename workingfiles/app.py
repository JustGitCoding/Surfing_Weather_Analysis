# Dependencies
import datetime as dt
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

# set up database engine
# connect_args needed because Python is a single thread application
## the other option is to open session = Session(engine) within each function
engine = create_engine("sqlite:///../Resources/hawaii.sqlite", connect_args={'check_same_thread': False})
inspector = inspect(engine)

# Reflect database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Create a new flask app 'instance'
app = Flask(__name__)

# define 'starting point' a.k.a the 'root'
@app.route('/')  ## the '/' denotes that we want to put our data at the root of our routes
# create a function that i want in this specific route
def welcome():
    return ("""
    Welcome to the Climate Analysis API!<br>
    Available Routes:<hr>
    <a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a><br>
    <a href="/api/v1.0/stations">/api/v1.0/stations</a><br>
    <a href="/api/v1.0/tobs">/api/v1.0/tobs</a><br>
    <a href="/api/v1.0/temp/start/end">/api/v1.0/temp</a><br>
    """)

@app.route('/api/v1.0/precipitation')
def precipitation():

    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)


@app.route('/api/v1.0/stations')
def stations():

    results = session.query(Station.station).all()
    stations = list(np.ravel(results)) # unravel results into a one-dimensional array and convert the array to a list
    return jsonify(stations=stations)

@app.route('/api/v1.0/tobs')
def temps_monthly():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)
    
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == '__main__':
    # app.debug = True
    app.run(debug=True)
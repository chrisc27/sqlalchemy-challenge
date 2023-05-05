# Import the dependencies.
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs")


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) 
    to a dictionary using date as the key and prcp as the value."""
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    past_date = '2016-08-23'

    # Perform a query to retrieve the data and precipitation scores
    last_year = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).where(Measurement.date >= past_date)

    #close session
    session.close()

    # Convert the query results to a dictionary
    dict_prcp = {}
    for record in last_year:
        dict_prcp[record.date] = record.prcp
    
    return jsonify(dict_prcp)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""

    # Create our session (link) from Python to the DB
    session2 = Session(engine)

    # Get station query 
    result = session2.query(Station)

    #close session
    session2.close()

    # Get stations as a list
    station_list = []
    for i in result:
        station_list.append(i.name)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Query the dates and temperature observations of the most-active station for the previous year of data."""

    # Create our session (link) from Python to the DB
    session3 = Session(engine)

    # List the stations and their counts in descending order.
    station_counts = session3.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).all()
    station_counts = sorted(station_counts, reverse=True, key=lambda tup: tup[1])

    #Get most active station
    most_active = station_counts[0][0]

    past_date = '2016-08-23'

    # Get data for most active station in past year
    last_year2 = session3.query(Measurement).where(Measurement.station == most_active).where(Measurement.date >= past_date).all()
    
    #close session
    session3.close()

    # Convert the query results to a dictionary
    dict_temp = {}
    for record in last_year2:
        dict_temp[record.date] = record.tobs
    
    return jsonify(dict_temp)

if __name__ == "__main__":
    app.run(debug=True)
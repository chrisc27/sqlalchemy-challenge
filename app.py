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
    return ()

if __name__ == "__main__":
    app.run(debug=True)
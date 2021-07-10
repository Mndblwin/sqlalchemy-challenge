import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
newBase = automap_base()
# reflect the tables
newBase.prepare(engine, reflect=True)

# Save reference to the table

Measurement = newBase.classes.measurement
Station = newBase.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query all precipitation and dates
    results = session.query(newBase.measurement, newBase.date).all()

    session.close()

    return jsonify(results)


@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(newBase.station).all()

    session.close()

    return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Tobs"""
    # Query all stations
    results = session.query(newBase.station).all()

    session.close()


    # Create a dictionary from the row data and append to a list of all_passengers
    all_weather = []
    for precipitation, station, tobs in results:
        weather_dict = {}
        weather_dict["Precipitation"] = precipitation
        weather_dict["station"] = station
        weather_dict["tobs"] = tobs
        all_weather.append(weather_dict)

    return jsonify(all_weather)


if __name__ == '__main__':
    app.run(debug=True)

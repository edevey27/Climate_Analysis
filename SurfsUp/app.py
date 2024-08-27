# Import the dependencies.
import datetime as dt
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine)

Measurements = Base.classes.measurement
Stations = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/home")
def welcome():
    return (
        f"WELCOME TO THE HAWAII CLIMATE ANALYSIS API<br/>",
        f"AVAILABLE ROUTES:<br/>",
        f"/api/v1.0/precipitation<br/>",
        f"/api/v1.0/tobs<br/>",
        f"/api/v1.0/temp/start<br/>",
        f"/api/v1.0/temp/start/end<br/>",
        f"<p>'start' and 'end' date should be in the format MMDDYYYY.</p>"
    )   
@app.route("/api/v1.0/precipitation")
def  precipitation():
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precipitation = session.query(Measurements.date, Measurements.prcp).\
        filter(Measurements.date >= previous_year).all()

    session.close()
    precip = {date: prcp for date, prcp in precipitation}

    return jsonify(precip)
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Stations.station).all()
    session.close()
    stations = list(np.ravel(results))

    return jsonify(Stations=stations)
  


@app.route("/api_v1.0/tobs")
def temp_monthly():
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurements.tobs).\
        filter(Measurements.station == "USC00519281").\
        filter(Measurements.date >= previous_year).all()

    session.close()

    temps = list(np.ravel(results))

    return jsonify(temps=temps)

@app.route("/api_v1.0/temp/<start>")
@app.route("/api_v1.0/temp/<start>/<end>")
def stats(start=None, end=None):

    sel = [func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)]
    if not end:
        start = dt.datetime.strptime(start, "%m%d%Y")
        results = session.query(*sel).\
            filter(Measurements.date >= start).all()

        session.close()

        temps = list(np.ravel(results))
        return jsonify(temps=temps)    
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")

    results = session.query(*sel).\
        filter(Measurements.date >= start).\
        filter(Measurements.date <= end).all()
    
    session.close()
    temps = list(np.ravel(results))
    returnjsonify(temps=temps)

if __name__ == "__main__":
        app.run(debug=True)  


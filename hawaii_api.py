from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)
app.config['JSON_SORT_KEYS']=False

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()

    all_precip = []
    for date, prcp in results:
        all_precip_d = {}
        all_precip_d["date"] = date
        all_precip_d["prcp"] = prcp
        all_precip.append(all_precip_d)

    return jsonify(all_precip)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results2 = session.query(Station.station).all()

    return jsonify(results2)

@app.route("/api/v1.0/tobs")
def temps():
    session = Session(engine)
    results3 = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()

    return jsonify(results3)

@app.route("/api/v1.0/<start_date>")
def calc_temps(start_date):
    session = Session(engine)
    results4 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
    return jsonify(results4)

@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps2(start_date, end_date):
    session = Session(engine)
    results5 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    return jsonify(results5)


if __name__ == "__main__":
    app.run(debug=True)
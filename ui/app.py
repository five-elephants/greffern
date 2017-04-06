from flask import Flask,render_template
import daq.db as db
import daq.acquire as acq
import datetime
from sqlalchemy import and_,or_,not_
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html

app = Flask(__name__)

def get_rows(start, end):
    if not start is None and not end is None:
        try:
            fmt = '%Y-%m-%d-%H-%M'
            dt_start = datetime.datetime.strptime(start, fmt)
            dt_end = datetime.datetime.strptime(end, fmt)
        except(ValueError):
            return "Error in time range"

        clause = db.temperatures.select().where(and_(
            db.temperatures.c.timestamp >= dt_start,
            db.temperatures.c.timestamp < dt_end
        )).order_by(db.temperatures.c.timestamp)
    else:
        clause = db.temperatures.select()\
            .order_by(db.temperatures.c.timestamp)

    rows = db.con.execute(clause)
    return rows

def generate_table(start, end):
    rows = get_rows(start, end)
    if rows is None:
        rows = []
    return render_template('temp_table.html', rows=rows)

@app.route('/acquire')
def acquire():
    temps = acq.read_sensors()
    acq.update_db(temps)
    return str(temps)

@app.route('/table')
@app.route('/table/<string:start>/<string:end>')
def index(start=None, end=None):
    return generate_table(start, end)

@app.route('/temp-plot')
def temp_plot():
    sensors_rows = db.con.execute(db.sensors.select())

    p = figure(
        title='Temperaturverlauf letzte 7 Tage',
        x_axis_label='Datum und Zeit',
        x_axis_type='datetime',
        y_axis_label='Temperatur [Celsius]'
    )

    colors = ['blue', 'red', 'green', 'orange']
    for color,sensor_row in zip(colors, sensors_rows):
        now = datetime.datetime.now()
        last_week = now - datetime.timedelta(days=7)

        clause = db.temperatures.select().where(and_(
            db.temperatures.c.timestamp >= last_week,
            db.temperatures.c.timestamp < now,
            db.temperatures.c.sensor_id == sensor_row.id
        )).order_by(db.temperatures.c.timestamp)

        data = db.con.execute(clause).fetchall()

        xs = [ x.timestamp for x in data ]
        ys = [ x.temperature for x in data ]

        p.line(xs, ys, legend=sensor_row.uid, line_color=color)

    html = file_html(p, CDN, "temperature plot")
    return html

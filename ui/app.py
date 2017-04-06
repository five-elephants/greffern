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
    rows = get_rows(None, None)

    if not rows is None:
        xs = {}
        ys = {}
        for row in rows:
            if row.sensor_id in xs:
                xs[row.sensor_id].append(row.timestamp)
            else:
                xs[row.sensor_id] = [ row.timestamp ]

            if row.sensor_id in ys:
                ys[row.sensor_id].append(row.temperature)
            else:
                ys[row.sensor_id] = [ row.temperature ]

        p = figure(x_axis_type='datetime')
        #p.line([0, 1, 2, 3], [1, 0, 1, 0])
        for sens in xs.keys():
            p.line(xs[sens], ys[sens])
        html = file_html(p, CDN, "temperature plot")
        return html
    else:
        return "No data found"

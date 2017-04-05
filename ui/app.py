from flask import Flask,render_template
import daq.db as db
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
        clause = db.temperatures.select()

    rows = db.con.execute(clause)

def generate_table(start, end):
    rows = get_rows(start, end)
    return render_template('temp_table.html', rows=rows)


@app.route('/table')
@app.route('/table/<string:start>/<string:end>')
def index(start=None, end=None):
    return generate_table(start, end)

@app.route('/temp-plot')
def temp_plot():
    rows = get_rows(None, None)

    p = figure()
    p.line([1, 2, 3, 4], [4, 3, 1, 2])
    html = file_html(p, CDN, "temperature plot")
    return html

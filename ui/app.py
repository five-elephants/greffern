# coding=utf-8

import flask as fl
import flask_login as fll
import flask_bootstrap as flb
from flask_wtf.csrf import CSRFProtect
import daq.db_orm as db
import daq.acquire as acq
import user
import forms
import datetime
from sqlalchemy import and_,or_,not_
import etl
import plots
import yaml
import babel
from bokeh.resources import CDN
from bokeh.embed import components
from functools import update_wrapper


with open('/home/john/config.yml', 'r') as f:
    config = yaml.load(f)

login_manager = fll.LoginManager()
login_manager.login_view = 'login'
csrf = CSRFProtect()

app = fl.Flask(__name__)
app.secret_key = config['secret_key']

login_manager.init_app(app)
csrf.init_app(app)
flb.Bootstrap(app)


def nocache(f):
    """ Decorator to disable caching """
    def new_func(*args, **kwargs):
        resp = fl.make_response(f(*args, **kwargs))
        resp.cache_control.no_cache = True
        return resp
    return update_wrapper(new_func, f)

@login_manager.user_loader
def load_user(user_id):
    defuser = user.DefaultUser()
    if user_id == defuser.get_id():
        return defuser 
    else:
        return None

def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    return value.strftime(format)

def timedeltaformat(value):
    delta = value - datetime.datetime.now()
    return babel.dates.format_timedelta(delta, add_direction=True, locale='de_DE')

app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['timedeltaformat'] = timedeltaformat
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        if form.username.data == config['default_user']['name'] and form.password.data == config['default_user']['password']:
            u = user.DefaultUser()
            fll.login_user(u)

            fl.flash('Eingeloggt')

            next = fl.request.args.get('next')
            return fl.redirect(next or fl.url_for('index'))
        else:
            #return '{} {}'.format(form.username.data, form.password.data)
            return fl.abort(400)
    return fl.render_template('login.html', form=form)

@app.route('/logout')
def logout():
    fll.logout_user()
    return fl.redirect(fl.url_for('index'))


@app.route('/')
@fll.login_required
def index():
    session = db.Session()
    sensors = session.query(db.Sensor).all()
    return fl.render_template('index.html', sensors=sensors)
    

def get_rows(start, end):
    session = db.Session()
    q = session.query(db.Temperature)

    if not start is None and not end is None:
        try:
            fmt = '%Y-%m-%d-%H-%M'
            dt_start = datetime.datetime.strptime(start, fmt)
            dt_end = datetime.datetime.strptime(end, fmt)
        except(ValueError):
            return "Error in time range"

        q = q.filter(db.Temperature.timestamp >= dt_start,
                     db.Temperature.timestamp < dt_end)

    return q.order_by(db.Temperature.timestamp).all()

def generate_table(start, end):
    rows = get_rows(start, end)
    if rows is None:
        rows = []
    return fl.render_template('temp_table.html', rows=rows)

@app.route('/acquire')
@fll.login_required
def acquire():
    temps = acq.read_sensors()
    acq.update_db(temps)
    return str(temps)

@app.route('/table')
@app.route('/table/<string:start>/<string:end>')
@fll.login_required
def table(start=None, end=None):
    return generate_table(start, end)

@app.route('/del_alert/<int:id>')
@fll.login_required
def delete_alert(id):
    session = db.Session()
    tgt = session.query(db.Alert).filter(db.Alert.id == id).one()
    session.delete(tgt)
    session.commit()

    fl.flash('Alarm {} gelöscht.'.format(tgt.name))
    return fl.redirect('/temperatur')

@app.route('/temperatur', methods=['POST', 'GET'])
@app.route('/temp-plot')
@fll.login_required
def temp_plot():
    session = db.Session()
    sensors = session.query(db.Sensor).\
        order_by(db.Sensor.id).\
        all()

    create_alert_form = forms.CreateAlertForm()
    create_alert_form.sensor.choices = [ 
        (s.id,plots.make_label(s)) for s in sensors
    ]
    if create_alert_form.validate_on_submit():
        alert = db.Alert(
            name=create_alert_form.name.data,
            sensor_id=create_alert_form.sensor.data,
            notify_email=create_alert_form.notify_email.data,
            above_trigger=create_alert_form.trigger_above.data,
            below_trigger=create_alert_form.trigger_below.data
        )

        session.add(alert)
        session.commit()

    now = datetime.datetime.now()
    last_week = now - datetime.timedelta(days=7)
    data = [
        session.query(db.Temperature).\
            filter(db.Temperature.timestamp >= last_week).\
            filter(db.Temperature.timestamp < now).\
            filter(db.Temperature.sensor == sensor).\
            order_by(db.Temperature.timestamp)
        for sensor in sensors
    ]
    labels = [ sensor.uid if sensor.name is None else sensor.name for sensor in sensors ]

    script, div = components(plots.temp_plot(labels, data))

    return fl.render_template('temperatur.html',
        script=script,
        div=div,
        resources=CDN,
        sensors=sensors,
        create_alert_form=create_alert_form)

@app.route('/explorer')
@fll.login_required
def explorer():
    labels, data, date_range = etl.month_by_day()
    week_script, week_div = components(plots.month_by_day(labels, data, date_range))

    labels, data, date_range = etl.year_by_month()
    year_script, year_div = components(plots.year_by_month(labels, data, date_range))

    return fl.render_template('explorer.html',
        scripts=[week_script, year_script],
        divs   =[week_div, year_div],
        resources=CDN)

@app.route('/webcam/<path:filename>')
@nocache
@fll.login_required
def webcam(filename):
    return fl.send_from_directory('/webcam', filename)

@app.route('/camera')
@fll.login_required
def camera():
    return fl.render_template('camera.html')


@app.route('/setup', methods=['POST', 'GET'])
@fll.login_required
def setup():
    session = db.Session()

    form = forms.UpdateSensorForm()
    if form.validate_on_submit():
        sensor = session.query(db.Sensor).\
            filter(db.Sensor.id == form.sensor_id.data).\
            one()
        sensor.name = form.name.data
        sensor.location = form.location.data
        session.commit()

        return fl.redirect(fl.url_for('setup'))

    sensors = session.query(db.Sensor).\
        order_by(db.Sensor.id).\
        all()
    update_sensor_forms = [
        forms.UpdateSensorForm(sensor_id=x.id,
                               name=x.name,
                               location=x.location)
        for x in sensors
    ]
    return fl.render_template('setup.html',
            data=zip(update_sensor_forms, sensors))



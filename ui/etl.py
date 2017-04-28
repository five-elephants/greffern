import daq.db_orm as db
import datetime
import plots

def next_month(x):
    if x.month == 12:
        return x.replace(year=x.year+1, month=1)
    else:
        return x.replace(month=x.month+1)


def month_by_day(year, month):
    session = db.Session()
    sensors = session.query(db.Sensor).\
        order_by(db.Sensor.id).\
        all()

    first_of_month = datetime.datetime(year=year, month=month, day=1)
    days = (next_month(first_of_month) - datetime.timedelta(days=1)).day
    data = [
        [
            session.query(db.Temperature).\
                filter(db.Temperature.timestamp >= first_of_month + datetime.timedelta(days=d)).\
                filter(db.Temperature.timestamp < first_of_month + datetime.timedelta(days=d+1)).\
                filter(db.Temperature.sensor == sensor).\
                order_by(db.Temperature.timestamp)
            for d in range(days)
        ]
        for sensor in sensors
    ]
    labels = [ plots.make_label(s) for s in sensors ]
    date_range = (first_of_month, next_month(first_of_month))

    return labels, data, date_range


def year_by_month(year, month):
    session = db.Session()
    sensors = session.query(db.Sensor).\
        order_by(db.Sensor.id).\
        all()

    first_of_year = datetime.datetime(year=year, month=1, day=1)

    starts = [ first_of_year.replace(month=m) for m in range(1, 13) ]
    data = [
        [
            session.query(db.Temperature).\
                filter(db.Temperature.timestamp >= start).\
                filter(db.Temperature.timestamp < next_month(start)).\
                filter(db.Temperature.sensor == sensor).\
                order_by(db.Temperature.timestamp)
            for start in starts
        ]
        for sensor in sensors
    ]
    labels = [ plots.make_label(s) for s in sensors ]
    date_range = (first_of_year, next_month(first_of_year.replace(month=12)))

    return labels, data, date_range

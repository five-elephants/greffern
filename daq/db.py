import sqlalchemy
from sqlalchemy import Table,Column,Integer,String,DateTime,Float,ForeignKey

def connect(user, password, db, host='localhost', port='5432'):
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    con = sqlalchemy.create_engine(url, client_encoding='utf8')
    meta = sqlalchemy.MetaData(bind=con, reflect=False)

    return con,meta


con, meta = connect('john', 'you!know%nothing', 'house')

sensors = Table('sensors', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('uid', String, unique=True),
    Column('location', String))

temperatures = Table('temperatures', meta,
    Column('id', Integer, primary_key=True),
    Column('timestamp', DateTime),
    Column('sensor_id', ForeignKey('sensors.id')),
    Column('temperature', Float))

meta.create_all()

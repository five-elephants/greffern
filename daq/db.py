import sqlalchemy
from sqlalchemy import Table,Column,Integer,String,DateTime,Float

def connect(user, password, db, host='localhost', port='5432'):
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    con = sqlalchemy.create_engine(url, client_encoding='utf8')
    meta = sqlalchemy.MetaData(bind=con, reflect=False)

    return con,meta


con, meta = connect('john', 'you!know%nothing', 'house')


temperatures = Table('temperatures', meta,
    Column('id', Integer, primary_key=True),
    Column('timestamp', DateTime),
    Column('sensor_id', String),
    Column('temperature', Float))

meta.create_all()

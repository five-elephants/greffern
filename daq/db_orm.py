import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Sequence,Column,Integer,String,DateTime,Float,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker

def connect(user, password, db, host='localhost', port='5432'):
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    engine = sqlalchemy.create_engine(url, client_encoding='utf8', echo=False)
    return engine

engine = connect('john', 'you!know%nothing', 'house')

Base = declarative_base()
Session = sessionmaker(bind=engine)

class Sensor(Base):
    __tablename__ = 'sensors'

    id = Column(Integer, Sequence('sensors_id_seq'), primary_key=True)
    name = Column(String)
    uid = Column(String, unique=True)
    location = Column(String)


class Temperature(Base):
    __tablename__ = 'temperatures'

    id = Column(Integer, Sequence('temperatures_id_seq'), primary_key=True)
    timestamp = Column(DateTime)
    sensor_id = Column(ForeignKey('sensors.id'))
    temperature = Column(Float)

    sensor = relationship('Sensor', back_populates='temperatures')

Sensor.temperatures = relationship("Temperature",
        order_by=Temperature.timestamp,
        back_populates='sensor')


class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(Integer,
                Sequence('alerts_id_seq'),
                primary_key=True,
                nullable=False)
    name = Column(String, nullable=False)
    sensor_id = Column(ForeignKey('sensors.id'), nullable=False)
    below_trigger = Column(Float)
    above_trigger = Column(Float)
    notify_email = Column(String)

    sensor = relationship('Sensor', back_populates='alerts')

Sensor.alerts = relationship('Alert',
    order_by=Alert.id,
    back_populates='sensor')

Base.metadata.create_all(engine)

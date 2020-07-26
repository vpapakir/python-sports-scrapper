#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
     import ConfigParser
except Exception as exc_cp:
     import configparser
import os
import sqlalchemy as sqla
import sqlalchemy.types as sqltypes
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Races(Base):
    __tablename__ = 'races'

    recordid = sqla.Column(sqltypes.Integer, primary_key = True)
    racedate = sqla.Column(sqltypes.TIMESTAMP)
    racevenue = sqla.Column(sqltypes.VARCHAR(30), nullable = False)
    racenumber = sqla.Column(sqltypes.Integer)
    horseid = sqla.Column(sqltypes.Integer)
    horsename = sqla.Column(sqltypes.VARCHAR(50), nullable = False)
    price = sqla.Column(sqltypes.Numeric(6,2), nullable = False, default = 0)
    dlr = sqla.Column(sqltypes.Integer, nullable = False)
    nr = sqla.Column(sqltypes.Numeric(6,2), nullable = False)
    nr_fin = sqla.Column(sqltypes.Numeric(2,1), nullable = True, default=None)


# connect to the MySQL db server
try:
    config = ConfigParser.ConfigParser()
except Exception as exc_cp:
    config = configparser.ConfigParser()

config_path = os.getcwd()
config.read(os.path.join(config_path, 'config/config.cfg'))
dbuser = config.get('mysqldb', 'dbuser')
dbpass = config.get('mysqldb', 'dbpass')
dbhost = config.get('mysqldb', 'dbhost')
dbname = config.get('mysqldb', 'dbname')

conn_str = ''.join(['mysql+oursql://', dbuser, ':', dbpass,
                    '@', dbhost])
engine = sqla.create_engine(conn_str) # connect to server

engine.execute('use ' + dbname)

Base.metadata.create_all(engine)

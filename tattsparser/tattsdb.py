#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# tattsdb.py #

import ConfigParser
import os
import datetime
import sqlalchemy as sqla
import sqlalchemy.types as sqltypes
import sqlalchemy.sql.functions as sqlfunc
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class TattsRaces(Base):
    __tablename__ = 'tattsraces'

    recordid = sqla.Column(sqltypes.Integer, primary_key=True)
    parsedate = sqla.Column(
        sqltypes.DateTime,
        server_default=sqlfunc.current_timestamp(),
        nullable=False,
    )
    racevenue = sqla.Column(sqltypes.VARCHAR(30), nullable=False)
    racenumber = sqla.Column(sqltypes.Integer, nullable=False)
    horseid = sqla.Column(sqltypes.Integer, nullable=False)
    horsename = sqla.Column(sqltypes.VARCHAR(50), nullable=False)
    rating = sqla.Column(sqltypes.Integer, nullable=False)
    rating_fin = sqla.Column(sqltypes.Numeric(2, 1), nullable=True, 
                             default=None)


# connect to the MySQL db server
config = ConfigParser.ConfigParser()
config_path = '{0}/public_html/application/python_scrapers'.format(os.environ['HOME'])
config.read(os.path.join(config_path, 'config/config.cfg'))
dbuser = config.get('mysqldb', 'dbuser')
dbpass = config.get('mysqldb', 'dbpass')
dbhost = config.get('mysqldb', 'dbhost')
dbname = config.get('mysqldb', 'dbname')

conn_str = ''.join(['mysql+oursql://', dbuser, ':', dbpass,
                    '@', dbhost])
engine = sqla.create_engine(conn_str) # connect to db server

engine.execute('use ' + dbname)

Base.metadata.create_all(engine)

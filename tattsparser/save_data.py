#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import ConfigParser
import os
import logging
import re
import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker

from tattsdb import Base, TattsRaces


logging.basicConfig()
logging.getLogger('sqla.engine').setLevel(logging.DEBUG)

# save to MySQL
def save_data(venues):
    # get db config data
    config = ConfigParser.ConfigParser()
    config_path = '/home/moneyinmotioncom/public_html/application/python_scrapers'
    config.read(os.path.join(config_path, 'config/config.cfg'))
    dbuser = config.get('mysqldb', 'dbuser')
    dbpass = config.get('mysqldb', 'dbpass')
    dbhost = config.get('mysqldb', 'dbhost')
    dbname = config.get('mysqldb', 'dbname')

    # connect to the MySQL server and the db
    conn_str = ''.join(['mysql+oursql://', dbuser, ':', dbpass,
                        '@', dbhost, '/', dbname])
    engine = sqla.create_engine(conn_str)#, echo=True)

    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)

    # start session
    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit(). If you're not happy about the changes, you can
    # revert all of them back to the last commit by calling
    # session.rollback()
    session = DBSession()

    # insert data into the table
    for ven, races in venues.iteritems():
        venue = ven
        for race in races:
            for race_number, horses in race.iteritems():
                race_num = race_number
                for horse in horses:
                    # prepare data for saving
                    horse_num = horse['horse_number']
                    horse_name = horse['horse_name']
                    rating = horse['rating']

                    new_record = TattsRaces(
                        racevenue = venue,
                        racenumber = int(race_num),
                        horseid = horse_num,
                        horsename = horse_name,
                        rating = rating,
                        rating_fin = horse['rating_fin'],
                    )

                    session.add(new_record)

    session.commit()
    session.close_all()


if __name__ == '__main__':
    save_data(0)

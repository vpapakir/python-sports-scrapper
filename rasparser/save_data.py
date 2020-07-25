import ConfigParser
import os
import re
import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker

from rasparserdb import Base, Races


# save to MySQL
def save_data(all_races):
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
    engine = sqla.create_engine(conn_str)

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
    for ven in all_races:
    	for race in ven:
            # prepare data for saving
            pr = re.findall('\d+\.\d+', race['pr'])
            race_num = race['race_num']
            horse_num = race['horse_number']
            horse_name = race['horse_name']
            venue = race['venue'].strip()
            dlr = race['dlr']
            nr = race['nr']
            nr_fin = race['nr_fin']

            if pr == []:
                pr.append(0.0)

            new_record = Races(
                racevenue = venue,
                racenumber = int(race_num),
                horseid = int(horse_num),
                horsename = horse_name,
                price = float(pr[0]),
                dlr = int(dlr),
                nr = float(nr),
                nr_fin = nr_fin,
            )

            session.add(new_record)

    session.commit()
    session.close()

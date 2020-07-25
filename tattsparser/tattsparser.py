#!/usr/bin/python
# -*- encoding=utf-8 -*-

import json
import os
import pytz
import random
import re
import requests
import time
import urlparse
from bs4 import BeautifulSoup as bs
from datetime import datetime

import final_rating
from requestheaders import Headers
from save_data import save_data


START_URL = 'https://tatts.com'
def main():
    # define urls
    racing_page = ''.join([START_URL, '/racing/'])

    soup = get_page_content(racing_page)
    print(soup)
    table = soup.find('table', {'id': 'page_R1'})
    
    # find all links, which match a pattern
    link_pattern = re.compile('^/racing/\d{4}/\d{1,2}/\d{1,2}/[a-zA-Z]{1}R$',
                              re.IGNORECASE)
    links = table.find_all('a', {'href': link_pattern})
    random.shuffle(links)
    hrefs = []
    for link in links:
        hrefs.append(link['href'])

    return hrefs


def get_races(hrefs):
    race_list = []
    # extract data from cells
    for href in hrefs:
        race_info = {}
        race_url = ''.join([START_URL, href])
        race_number = href.split('/')[-1]
        race_info[race_number] = get_horses(race_url)
        race_list.append(race_info)

    return race_list


def get_horses(race_url):
    soup = get_page_content(race_url)

    # find starting tr
    start_tr = soup.find('tr', {'id': 'fieldRow'})
    # extract siblings
    horses_list = []
    for sib in start_tr.find_previous_siblings('tr'):
        sib_tds = [td.text.strip().encode('utf-8', errors='ignore') 
                   for td in sib.find_all('td')]
        if len(sib_tds) == 28:
#            print('sib_tds[-2]: {0}'.format(sib_tds[-2]))
            try:
                horse_number = int(sib_tds[1])
                rating = float(sib_tds[-2])
            except ValueError:
                print('Either horse_number ({0}) or'
                      ' rating: ({1}) is not a number.'\
                      .format(horse_number, rating))
                continue

            rating_fin = final_rating.get_final_rating(rating, horse_number)
            horses_data = {
                'horse_number': horse_number,
                'horse_name': sib_tds[2],
                'rating': rating,
                'rating_fin': rating_fin,
            }

            horses_list.append(horses_data)

    return horses_list


def get_page_content(url):
    # generate headers
    headers = Headers()
    hdr = headers.generateRandomHeaders()
    page = requests.get(url, headers = hdr)

    # parse page
    soup = bs(page.text, 'lxml')
    return soup    


if __name__ == '__main__':
    # try to scrape 3 times with 60 sec interval
    count_tries = 1
    while count_tries <= 3:
        try:
            brisbane_timezone = pytz.timezone('Australia/Brisbane')
            brisbane_now = datetime.now(brisbane_timezone)
            print(brisbane_now.strftime('%c'))
#            print('Parsing ...')
            hrefs = main()
            # loop through links and extract the url
            venues = {}
            cnt = 0
            for href in hrefs:
                cnt += 1
                venue_url = ''.join([START_URL, href])
                venue_soup = get_page_content(venue_url)

                venue = venue_soup.title.text
                print('Venue: {0}'.format(venue))

                # collect all races' rows from the table
                # find all links, which match a pattern
                race_path = urlparse.urlparse(venue_url).path
                link_pattern = re.compile(r'%s/\d$' % race_path, re.IGNORECASE)
                races = venue_soup.find_all('a', {'href': link_pattern})
                races_hrefs = set()
                for race in races:
                    races_hrefs.add(race['href'])

                # get race data
                races = get_races(races_hrefs)
                print('Parsed {0} races.'.format(len(races)))

                venues[venue] = races

            print('Parsing finished.')

            save_data(venues)
            print('Data saved!')
            print('Finished!\n')
        except Exception as ex:
            if count_tries == 3:
                raise

            print('{0}! Retrying ...'.format(ex))
            time.sleep(180)
            count_tries += 1
            continue

        break

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pytz
import re
import random
import requests
import time
from bs4 import BeautifulSoup as bs
from datetime import datetime

import final_nr
from requestheaders import request_header
from save_data import save_data


def main():
    # define urls
    start_url = 'http://www.racingandsports.com.au/en/form-guide/'

    # get web page
    hdr = request_header()
    page = requests.get(start_url, headers = hdr)
    soup = bs(page.text, 'lxml')

    # create a list
    all_races = []

    # get main div element
    main_div = soup.find('div', {'id': 'accordion36T'})

    td_accept = main_div.find_all('td', text='Acceptance')
    venues = {}
    for td in td_accept:
        anchor = td.previous_sibling.find('a', class_='nf')
        venue_id = re.search('\d+', anchor['href']).group()
        venue_name = anchor.text.strip()
        print('{0}: {1}'.format(venue_id, venue_name))
        venues[venue_id] = venue_name

    for item in venues.items():
        # parse tables' page
        venue_races = parse_data(start_url, item)
        all_races.append(venue_races)
        # make random delay to simulate a real user
        time.sleep(random.choice([x for x in range(3, 7)]))

    return all_races


def parse_data(start_url, venue):
    # create list
    venue_races = []

    # construct table url
    race_num = 1
    meeting_id = venue[0]
    venue_name = venue[1]
    table_url = ''.join([
        start_url,
        'neural.asp?raceno=',
        str(race_num),
        '&meetingid=',
        meeting_id,
    ])

    # get the table's page
    hdr = request_header()
    page = requests.get(table_url, headers=hdr)
    soup = bs(page.text, 'lxml')
    
    tbody = soup.find('tbody', {'id': 'offTblBdy'})
    tbody2 = soup.find('tbody', {'id': 'offTblBdy2'})
    # check if the tbody element exists
    while tbody and tbody2:

        # parse horse number and PR value
        trs = tbody.find_all('tr')
        # parse NR and DLR values from the second table
        trs2 = tbody2.find_all('tr')
        for tr in trs:
            horse = {
                'venue': venue_name,
                'race_num': race_num,
            }
            pr = tr.contents[7].text
            # do not parse row with empty price cells
            if len(pr) > 1:
                horse['horse_number'] = tr.contents[1].text
                horse['horse_name'] = tr.contents[2].text
                horse['pr'] = pr

                for tr2 in trs2:
                    horse_number2 = tr2.contents[0].text
                    if horse_number2 == horse['horse_number']:
                        horse['dlr'] = tr2.contents[-1].text
                        horse['nr'] = tr2.contents[2].text
                        horse['nr_fin'] = final_nr.get_final_nr(
                            horse['nr'], horse_number2)

                # add horse to the list
                venue_races.append(horse)
        
        # check if a new page exists
        race_num += 1
        table_url = ''.join([
            start_url,
            'neural.asp?raceno=',
            str(race_num),
            '&meetingid=',
            meeting_id,
        ])
        
        # get table's page
        hdr = request_header()
        page = requests.get(table_url, headers = hdr)
        soup = bs(page.text, 'lxml')
        tbody = soup.find('tbody', {'id': 'offTblBdy'})
        tbody2 = soup.find('tbody', {'id': 'offTblBdy2'})

    return venue_races


# execute
if __name__ == '__main__':
    # try to scrape 2 times if succeeds and 3 times if fails
    count_tries = 1
    count_fails = 1
    while count_tries <= 2 and count_fails <= 3:
        try:
            brisbane_timezone = pytz.timezone('Australia/Brisbane')
            brisbane_now = datetime.now(brisbane_timezone)
            print(brisbane_now.strftime('%c'))
#            print('Parsing data ...')
            
            # parse web pages
            all_races = main()
            print('Parsed %s venues.' % len(all_races))

#            print('Saving data to the database...')
            save_data(all_races)

            print('Data saved to the database.')

            print('Scraping succesful! Retrying ...')
            count_tries += 1
            time.sleep(30)
        except Exception as ex:
            if count_fails == 3:
                raise

            print('Scraping failed: {0}! Retrying ...'.format(ex))
            time.sleep(60)
            count_fails += 1
            count_tries -= 1
            continue

        if count_tries == 2:
            print('Finished!')
            break

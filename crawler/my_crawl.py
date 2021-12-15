import csv
import json
import traceback
import urllib
import time
from typing import Any
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import logging

logging.basicConfig(filename='my_log.log', level=logging.DEBUG)

def collect_urls(page_num: int) -> list:
    """
    Help fucnction for collecting links with congrsat letters from the
    http://kremlin.ru/events/president/letters web page.
    :param page_num: page number
    :return: list with links from input page
    """
    try:
        pres_letters = urlopen(f'http://kremlin.ru/events/president/letters/page/{page_num}')
        time.sleep(2)
    except urllib.error.HTTPError as err:
        logging.error(err)
        time.sleep(5)
        return collect_urls(page_num)
    parced_main = bs(pres_letters, 'html.parser')
    href_list = ['http://kremlin.ru/' + a['href'] for a in parced_main.find_all('a', href=True) if
                 'letters' in a['href'] and len(a['href'].split('/')) == 5]

    logging.error(f'len of the list of links {len(href_list)}')
    logging.error(f'len of the set of links {len(set(href_list))}')
    return href_list

def write_txt(title: str, content: str):
    """
    Help function for collect_and_write().
    Writes parced data in txt file separated by TITLE, CONTENT and END strings.
    """
    with open('congrats.txt', 'a') as my_handler:
        my_handler.write('\nTITLE\n')
        my_handler.write(title)
        my_handler.write('\nCONTENT\n')
        my_handler.write(content)
        my_handler.write('\nEND\n')


def collect_and_write(links_list: list):
    """
    Collects congrats texts and titles, writes them in txt file with write_txt
    :param links_list: list with links to congrats texts and titles
    """
    start_from = 0
    with open('config.json') as config_handler:
        curr_config = json.load(config_handler)
    if curr_config["last_index"] != 0:
        start_from = curr_config["last_index"]
        links_list = links_list[start_from:]

    for index, link in enumerate(links_list):
        letter = False
        try:
            letter = urlopen(link)
            time.sleep(2)
        except urllib.error.HTTPError as err:
            print(traceback.format_exc())
            logging.error(err)

        if letter:
            curr_config['last_index'] = index + start_from
            if index == (len(links_list) - 1):
                curr_config['last_index'] = 0
            with open('config.json', 'w') as config_writer:
                json.dump(curr_config, config_writer)

            parced_letter = bs(letter, 'html.parser')
            if parced_letter.find('div', 'read__place p-location') and \
                    parced_letter.find('div', 'read__place p-location').text == 'Поздравления':
                title = parced_letter.find('h1', 'entry-title p-name').text
                content = parced_letter.find('div', 'entry-content e-content read__internal_content').text
                write_txt(title, content)


if __name__=='__main__':

    with open('config.json') as config_handler:
        curr_config = json.load(config_handler)
        page_num = curr_config['last_page']

    with open('links.json') as links_handler:
        links_storage = json.load(links_handler)

    my_links = collect_urls(page_num)
    while my_links:
        links_storage["links"] += my_links
        with open('links.json', 'w') as links_writer:
            json.dump(links_storage["links"], links_writer)

        collect_and_write(my_links)

        curr_config['last_page'] += 1
        page_num = curr_config['last_page']
        with open('config.json', 'w') as config_writer:
            json.dump(curr_config, config_writer)

        my_links = collect_urls(page_num)

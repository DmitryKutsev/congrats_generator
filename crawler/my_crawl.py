import csv
import traceback
import urllib
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
    except urllib.error.HTTPError as err:
        logging.error(err)
        return []
    parced_main = bs(pres_letters, 'html.parser')
    href_list = ['http://kremlin.ru/' + a['href'] for a in parced_main.find_all('a', href=True) if
                 'letters' in a['href'] and len(a['href'].split('/')) == 5]
    print(href_list)
    print(len(href_list))
    print(len(set(href_list)))

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
    :param links_list: list with links to congrats texts and titles
    """
    for link in links_list:
        letter = False
        try:
            letter = urlopen(link)
        except urllib.error.HTTPError as err:
            print(traceback.format_exc())
            logging.error(err, )
        if letter:
            parced_letter = bs(letter, 'html.parser')
            if parced_letter.find('div', 'read__place p-location').text == 'Поздравления':
                title = parced_letter.find('h1', 'entry-title p-name').text
                content = parced_letter.find('div', 'entry-content e-content read__internal_content').text
                write_txt(title, content)
        else:
            pass


# collect_and_write([f'http://kremlin.ru//events/president/letters/67349'])


if __name__=='__main__':
    page_num = 1
    my_links = collect_urls(page_num)

    while my_links:
        collect_and_write(my_links)
        page_num += 1
        my_links = collect_urls(page_num)
        if page_num > 2:
            break
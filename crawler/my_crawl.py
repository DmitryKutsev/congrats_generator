import csv
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
# collect_urls(1)

def write_in_table(title, content):
    with open('congrats.csv', 'a', newline='') as csvfile:
        my_writer = csv.writer(csvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        my_writer.writerow([content, title])
        # for sentence in content.split('.'):
        #     my_writer.writerow([sentence, title])



def collect_texts(links: list) -> Any:
    # http://kremlin.ru//events/president/letters/67349
    letter = urlopen(f'http://kremlin.ru//events/president/letters/67349')
    parced_letter = bs(letter, 'html.parser')
    print(parced_letter.find('div', 'read__place p-location').text)
    if parced_letter.find('div', 'read__place p-location').text == 'Поздравления':
        # h1 class="entry-title p-name"
        print(parced_letter.find('h1', 'entry-title p-name').text)
        title = parced_letter.find('h1', 'entry-title p-name').text
        print('\n\n')
        print(parced_letter.find('div', 'entry-content e-content read__internal_content').text)
        content = parced_letter.find('div', 'entry-content e-content read__internal_content').text
        write_in_table(title, content)

    else:
        pass


collect_texts([])


# if __name__=='__main__':
#     page_num = 1
#     my_links = collect_urls(page_num)
#
#     while my_links:
#         write_texts(my_links)
#         page_num += 1
#         my_links = collect_urls(page_num)
import re
import time
from .utils import get_soup


year_base = 'https://www.imdb.com/search/title?title_type=feature&year={0}-01-01,{0}-12-31&start={1}&ref_=adv_nxt'
pattern = re.compile('[\d,]+ titles')


def yield_topmovie_title_idxs(year, max_num=3000, sleep=1.0, verbose=False):
    """
    Arguments
    ---------
    year : int or str
        For example, 2018
    max_num : int
        Maximum number movies to scrap

    Yields
    ------
    list of tuple, (title, idx)
    """

    last_num = get_total_number_of_movies(year)
    if last_num == -1:
        raise ValueError('Failed to get total number of movies')

    last_num = min(last_num, max_num)
    if verbose:
        print('Begin year = {}, / {} movies'.format(year, last_num), end='')

    for start in range(1, last_num + 1, 50):
        if verbose:
            print('\rScraping year = {}, {} / {} movies'.format(year, start, last_num), end='', flush=True)
        try:
            yield parse_a_page(year, start)
            time.sleep(sleep)
        except Exception as e:
            print(e)
            print('\nUnexpected exception. Sleep 10 minutes. year = {}, start = {}'.format(year, start))
            time.sleep(600)
    if verbose:
        print('\rScraping year = {0}, {1} / {1} movies was done'.format(year, last_num), flush=True)

def get_total_number_of_movies(year):
    try:
        url = year_base.format(year, 1)
        soup = get_soup(url)
        text = soup.select('div[class=desc] span')[0].text
        text = pattern.findall(text)[0].replace('titles', '').replace(',', '').strip()
        return int(text)
    except:
        return -1

def parse_a_page(year, start):
    url = year_base.format(year, start)
    soup = get_soup(url)
    divs = soup.select('div[class=lister-item-content]')
    title_idxs = [
        parse_title_idx_from_div(div) for div in divs]
    return title_idxs

def parse_title_idx_from_div(div):
    a = div.select('a[href^="/title/tt"]')[0]
    title = a.text.strip()
    idx = a.attrs.get('href', '').split('/?')[0].replace('/title/tt', '')
    idx = int(idx)
    return title, idx

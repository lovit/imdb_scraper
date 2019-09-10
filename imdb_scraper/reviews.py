import math
import time
from .utils import get_soup
from .utils import normalize_text
from .utils import idx_as_strf


reviews_base = 'https://www.imdb.com/title/tt{}/reviews/_ajax?sort=submissionDate&dir=desc&ref_=undefined&paginationKey={}'
front_base = 'https://www.imdb.com/title/tt{}/reviews/_ajax?sort=submissionDate'


def yield_reviews(idx, max_page=3, sleep=1.0, already_scraped=None, rescrap=False):
    """
    Arguments
    ---------
    idx : int or str
        Movie id
    max_page : int
        Maximum number of page.
        Maximum number of reviews is 25 x max_page
    sleep : float
        Sleep time [second]
    already_scraped : set of str
        Set of id of which already scraped.
        If rescrap is False and a id of scraped review in this
        function exists in 'already_scraped', then stop yielding.
    rescrap : Boolean
        If True, it scraps all reviews whether a id of review exists
        in 'already_scraped' or not.

    Yields
    -------
    list of JSON format reviews

    Usage
    -----
        for reviews in yield_reviews(idx):
            # do something
    """

    idx = idx_as_strf(idx)

    if already_scraped is None:
        already_scraped = set()

    # get number of reviews
    num_reviews = get_num_of_reviews(idx)
    if max_page > 0:
        max_page = min(max_page, math.ceil(num_reviews / 25))
    else:
        max_page = math.ceil(num_reviews / 25)

    # front page
    url = front_base.format(idx)
    soup = get_soup(url)
    datakey = parse_data_key(soup)
    yield parse_reviews_soup(soup)

    # loop
    stop = False
    for p in range(1, max_page):
        if stop:
            break
        time.sleep(sleep)
        url = reviews_base.format(idx, datakey)
        soup = get_soup(url)
        datakey = parse_data_key(soup)
        reviews = parse_reviews_soup(soup)
        if not rescrap:
            reviews_ = [review for review in reviews if not (review['id'] in already_scraped)]
            if len(reviews) != len(reviews_):
                stop = True
        else:
            reviews_ = reviews
        yield reviews_

def parse_data_key(soup):
    """
    Arguments
    ---------
    soup : bs4.BeautifulSoup
        From https://www.imdb.com/title/tt{}/reviews/_ajax?

    Returns
    -------
    data_key

    Usage
    -----
        url = 'https://www.imdb.com/title/tt0371746/reviews/_ajax?sort=submissionDate'
        soup = get_soup(url)
        parse_data_key(soup)
    """

    div = soup.select('div[class=load-more-data]')
    if not div:
        return None
    return div[0].attrs.get('data-key', '')

def get_num_of_reviews(idx):
    """
    Arguments
    ---------
    idx : str
        String format movie idx

    Returns
    -------
    Number of reviews
    """

    url = 'https://www.imdb.com/title/tt{}/reviews?'.format(idx)
    soup = get_soup(url)
    try:
        text = soup.select('div[class=header] span')[0].text
        text = text.replace('Reviews', '').replace(',', '').strip()
        return int(text)
    except Exception as e:
        return 0

def parse_reviews_soup(soup):
    """
    Arguments
    ---------
    soup : bs4.BeautifulSoup
        From https://www.imdb.com/title/tt{}/reviews/_ajax?

    Returns
    -------
    list of JSON format review

    Usage
    -----

        >>> url = 'https://www.imdb.com/title/tt0371746/reviews/_ajax?sort=submissionDate'
        >>> soup = get_soup(url)
        >>> parse_reviews_soup(soup)

        [{'content': 'Amazing. Just amazing. The MCU started off with a bang. Robert '
                    "Downey Jr.'s phenomenal performance is great, and with a "
                    'dangerous antagonist, Iron Man is bound for greatness. 0 out of 0 '
                    'found this helpful. Was this review helpful? Sign in to vote. '
                    'Permalink',
         'date': '25 January 2019',
         'id': 'rw4605666',
         'rating': '9',
         'title': 'Iron Man Review',
         'user': 'ur67856870'}
        {'content': 'A dynamic, inventive, thrilling, fun story with deep meaning, '
                    'complemented by a vibrant Robert Downey Jr. performance and cool '
                    'visual effects. John Favreau gave a flawless start to an awesome '
                    'franchise. 0 out of 0 found this helpful. Was this review '
                    'helpful? Sign in to vote. Permalink',
         'date': '23 January 2019',
         'id': 'rw4601717',
         'rating': '10',
         'title': 'Impressive start of an incredible universe',
         'user': 'ur98135771'}}]
    """

    def parse(div):
        try:
            review_id = div.attrs.get('data-review-id', '')
            title = normalize_text(div.select('a[class=title]')[0].text)
            user = div.select('span[class=display-name-link] a')[0].attrs.get('href', '').split('/?')[0].replace('/user/', '')
            date = div.select('span[class=review-date]')[0].text
            content = normalize_text(div.select('div[class=content]')[0].text)
            #return {'title': title, 'user': user, 'date': date, 'content': content, 'id': review_id}
            rating = div.select('span[class=rating-other-user-rating] span')[0].text.strip()
            return {'title': title, 'user': user, 'date': date, 'content': content, 'id': review_id, 'rating': rating}
        except Exception as e:
            return None

    reviews = []
    idx_set = set()
    for div in soup.select('div[class^=lister-item]'):
        review_id = div.attrs.get('data-review-id', '')
        if not review_id or review_id in idx_set:
            continue
        review = parse(div)
        if review is not None:
            reviews.append(review)
        idx_set.add(review_id)
    return reviews

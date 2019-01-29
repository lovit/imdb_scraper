from .utils import get_soup
from .utils import normalize_text


reviews_base = 'https://www.imdb.com/title/tt{}/reviews/_ajax?sort=submissionDate&dir=desc&ref_=undefined&paginationKey={}'
front_base = 'https://www.imdb.com/title/tt{}/reviews/_ajax?sort=submissionDate'

def parse_reviews(id):
    raise NotImplemented

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

        [{'content': "Amazing. Just amazing. The MCU started off with a bang. ...",
          'date': '25 January 2019',
          'id': 'rw4605666',
          'title': 'Iron Man Review',
          'user': 'ur67856870'},
         {'content': 'A dynamic, inventive, thrilling, fun story with deep meaning, ...",
          'date': '23 January 2019',
          'id': 'rw4601717',
          'title': 'Impressive start of an incredible universe',
          'user': 'ur98135771'}]
    """

    def parse(div):
        try:
            review_id = div.attrs.get('data-review-id', '')
            title = normalize_text(div.select('a[class=title]')[0].text)
            user = div.select('span[class=display-name-link] a')[0].attrs.get('href', '').split('/?')[0].replace('/user/', '')
            date = div.select('span[class=review-date]')[0].text
            content = normalize_text(div.select('div[class=content]')[0].text)
            return {'title': title, 'user': user, 'date': date, 'content': content, 'id': review_id}
        except Exception as e:
            print(e)
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
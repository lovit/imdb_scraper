from .utils import get_soup
from .utils import normalize_text
from .utils import idx_as_strf

main_base = 'https://www.imdb.com/title/tt{}/?ref_=fn_al_tt_1'


def parse_main(id):
    """
    Arguments
    ---------
    id : int
        Movie id

    Returns
    -------
    Json format information
    """

    url = main_base.format(idx_as_strf(id))
    soup = get_soup(url)

    informations = {}

    # title, year
    title, year = parse_title_year(soup)
    informations['Title'] = title
    informations['Year'] = year

    # directors
    directors = parse_director(soup)
    if directors:
        informations['Directors'] = directors

    # Plot Keywords & Genres
    for div in soup.select('div[id=titleStoryLine] div[class^=see-more]'):
        key = div.select('h4')
        if not key:
            continue
        key = normalize_text(key[0].text)
        values = div.select('a')
        values = [normalize_text(a.text) for a in values]
        values = [v for v in values if not v[:7] == 'See All']
        informations[key] = values

    # Others
    for block in soup.select('div[class=txt-block]'):
        h4 = block.select('h4')
        if not h4:
            continue

        key = h4[0].text
        value = block.text[len(key):].strip()
        if not value:
            continue

        key = normalize_text(key)
        value = normalize_text(value)

        if value[-8:] == 'See more':
            value = value[:-8].strip()
        if ' | ' in value:
            value = value.split(' | ')
            value = [v.strip() for v in value]
        informations[key] = value

    return informations

def parse_director(soup):
    directors = []

    for div in soup.select('div[class=credit_summary_item]'):
        h4 = div.select('h4')
        if not h4:
            continue
        if 'Director' in h4[0].text and div.select('a'):
            name = div.select('a')[0].text.strip()
            idx = div.select('a')[0].attrs.get('href', '').split('/?')[0].replace('/name/nm', '')
            try:
                idx = int(idx)
            except:
                idx = -1
            directors.append({'id': idx, 'name': name})

    return directors

def parse_title_year(soup):
    title = soup.select('div[class=title_wrapper] h1')[0].text.replace('\xa0', ' ').strip()
    year = ''
    if title[-6] == '(' and title[-1] == ')':
        year = title[-5:-1]
    return title, year
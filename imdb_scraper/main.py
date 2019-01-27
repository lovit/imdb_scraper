from .utils import get_soup
from .utils import normalize_text

main_base = 'https://www.imdb.com/title/tt{}'


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

    url = 'https://www.imdb.com/title/tt0371746/?ref_=fn_al_tt_1'.format(id)
    soup = get_soup(url)

    informations = {}

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
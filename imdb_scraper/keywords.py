from .utils import idx_as_strf
from .utils import get_soup


keyword_bases = 'https://www.imdb.com/title/tt{}/keywords?ref_=tt_stry_kw'


def parse_keywords(id):
    """
    Arguments
    ---------
    id : int
        Movie id

    Returns
    -------
    List of keywords (str format)
    """

    id = idx_as_strf(id)
    url = keyword_bases.format(id)
    soup = get_soup(url)
    trs = soup.select('table[class^=dataTable] div[class=sodatext]')
    keywords = [tr.text.strip() for tr in trs]
    return keywords
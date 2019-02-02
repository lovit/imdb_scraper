from .utils import get_soup
from .utils import normalize_text
from .utils import idx_as_strf

credit_base = 'https://www.imdb.com/title/tt{}/fullcredits?ref_=tt_cl_sm#cast'


def parse_credits(id):
    """
    Arguments
    ---------
    id : int
        Movie id

    Returns
    -------
    List of json format information
    """

    url = credit_base.format(idx_as_strf(id))
    soup = get_soup(url)

    marker = '...'
    credits = []

    trs = soup.select('table[class=cast_list] tr')

    for tr in trs:

        text = tr.text.replace('\n', '').replace('\t','').strip()
        if not text or not marker in text:
            continue
        idx = tr.select('a[href^="/name/nm"]')
        if idx:
            idx = idx[0].attrs.get('href', '').split('/?')[0]
            idx = idx.replace('/name/nm','')
            try:
                idx = int(idx)
            except:
                idx = -1
        else:
            idx = -1

        name, role = text.split(marker, 1)
        name = normalize_text(name)
        role = normalize_text(role)
        order= len(credits) + 1
        credits.append({'name': name, 'id': idx, 'role': role, 'order': order})

    return credits

import re
from .utils import get_soup
from .utils import normalize_text
from .utils import idx_as_strf


quote_base = 'https://www.imdb.com/title/tt{}/quotes/?tab=qt&ref_=tt_trv_qu'
pattern = re.compile('[\d,]+ of [\d,]+')


def parse_quotes(id):
    """
    Arguments
    ---------
    id : int
        Movie id

    Returns
    -------
    List of json format information
    """

    id = idx_as_strf(id)
    url = quote_base.format(id)
    soup = get_soup(url)

    quotes = []
    for div in soup.select('div[class=list] div[class^=quote]'):
        try:
            agree = parse_agree(div)
            for p in div.select('p'):
                quote = parse_quote_from_p(p)
                if not quote:
                    continue
                quote['agree'] = agree
            quotes.append(quote)
        except Exception as e:
            print(e)
            continue
#             break
    return quotes

def parse_agree(div):
    text = div.select('div[class=did-you-know-actions]')[0].text
    agree = pattern.findall(text)
    agree = agree[0] if agree else ''
    return agree

def parse_quote_from_p(p):
    character = p.select('span[class=character]')
    if character:
        character = character[0].text.strip()
    else:
        character = ''

    quote = p.text.strip()[len(character):]
    if quote[0] == ':':
        quote = quote[1:].strip()
    quote = normalize_text(quote)
    return {'character': character, 'quote': quote}
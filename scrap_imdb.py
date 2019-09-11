import argparse
import json
import os
import time

from imdb_scraper import parse_main
from imdb_scraper import parse_credits
from imdb_scraper import yield_reviews
from imdb_scraper import parse_keywords
from imdb_scraper import parse_quotes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str, default='./output', help='Output directory')
    parser.add_argument('--begin_year', type=int, default=1930, help='yyyy form')
    parser.add_argument('--end_year', type=int, default=2019, help='yyyy form')
    parser.add_argument('--sleep', type=float, default=10.0, help='yyyy form')
    parser.add_argument('--main', dest='scrap_main', action='store_true')
    parser.add_argument('--credits', dest='scrap_credits', action='store_true')
    parser.add_argument('--keywords', dest='scrap_keywords', action='store_true')
    parser.add_argument('--quotes', dest='scrap_quotes', action='store_true')
    parser.add_argument('--reviews', dest='scrap_reviews', action='store_true')
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.add_argument('--rescrap', dest='rescrap', action='store_true')
    parser.add_argument('--fast-update', dest='fastupdate', action='store_true',
        help='If True, this script scraps movie reviews which are not scraped before time')

    args = parser.parse_args()
    directory = args.directory
    begin_year = args.begin_year
    end_year = args.end_year
    sleep = args.sleep
    scrap_main = args.scrap_main
    scrap_credits = args.scrap_credits
    scrap_keywords = args.scrap_keywords
    scrap_quotes = args.scrap_quotes
    scrap_reviews = args.scrap_reviews
    debug = args.debug
    rescrap = args.rescrap
    fastupdate = args.fastupdate

    # check output directory
    directories = ['{}/main/', '{}/credits/', '{}/keywords/', '{}/quotes/', '{}/reviews/']
    directories = [d.format(directory) for d in directories]
    for d in directories:
        if not os.path.exists(d):
            os.makedirs(d)

    print('Scrap main    : {}'.format(scrap_main))
    print('Scrap credits : {}'.format(scrap_credits))
    print('Scrap keywords: {}'.format(scrap_keywords))
    print('Scrap quotes  : {}'.format(scrap_quotes))
    print('Scrap reviews : {}'.format(scrap_reviews))
    print('Fast update   : {}'.format(fastupdate))
    print('year          : {} ~ {}'.format(begin_year, end_year))

    for year in range(end_year, begin_year - 1, -1):

        id_list_path = 'movie_lists/{}.txt'.format(year)
        if not os.path.exists(id_list_path):
            print('List of {} year does not exist'.format(year))
            continue

        title_idxs = load_movie_idx(id_list_path)
        if debug:
            title_idxs = title_idxs[:3]

        n_movies = len(title_idxs)
        for i_movie, (title, idx) in enumerate(title_idxs):

            print('[{} / {}]: {} ({})'.format(i_movie + 1, n_movies, title, year))

            path = '{}/main/{}.json'.format(directory, idx)
            if (scrap_main and not os.path.exists(path)) or (scrap_main and rescrap):
                obj = parse_main(idx)
                save_json(obj, path)
                print('scrap {} main'.format(idx))
                time.sleep(1)

            path = '{}/credits/{}'.format(directory, idx)
            if (scrap_credits and not os.path.exists(path)) or (scrap_credits and rescrap):
                obj = parse_credits(idx)
                save_list_of_json(obj, path)
                print('scrap {} credits'.format(idx))
                time.sleep(1)

            path = '{}/keywords/{}'.format(directory, idx)
            if (scrap_keywords and not os.path.exists(path)) or (scrap_keywords and rescrap):
                obj = parse_keywords(idx)
                save_list(obj, path)
                print('scrap {} keywords'.format(idx))
                time.sleep(1)

            path = '{}/quotes/{}'.format(directory, idx)
            if (scrap_quotes and not os.path.exists(path)) or (scrap_quotes and rescrap):
                obj = parse_quotes(idx)
                save_list_of_json(obj, path)
                print('scrap {} quotes'.format(idx))
                time.sleep(1)

            path = '{}/reviews/{}'.format(directory, idx)
            if scrap_reviews:
                # set debug mode
                if debug:
                    max_page = 3
                else:
                    max_page = -1

                # load scraped reviews and initialize scrapeds
                if not os.path.exists(path) or rescrap:
                    reviews = []
                else:
                    reviews = load_reviews(path)
                scrapeds = {r['id'] for r in reviews}

                # reset scraped file
                if rescrap:
                    save_list_of_json([], path, op='w')

                for i_reviews, reviews in enumerate(yield_reviews(idx, max_page, sleep, scrapeds, rescrap)):
                    save_list_of_json(reviews, path, op='a')
                    print('\rscrap reviews of movie={} from {} pages ..'.format(idx, i_reviews + 1), end='', flush=True)
                if max_page > 0 and (i_reviews + 1 < max_page):
                    print('\rearly stop scraping review of movie={} from {} pages'.format(idx, i_reviews + 1))
                else:
                    print('\rscrap reviews of movie={} from {} pages was done.'.format(idx, i_reviews + 1))

            print('-'*40)
        print('done year = {} ({} ~ {})'.format(year, begin_year, end_year))

def load_movie_idx(path):
    try:
        with open(path, encoding='utf-8') as f:
            # skip head
            next(f)
            docs = [doc.split('\t') for doc in f]
            docs = [(doc[0], int(doc[1].strip())) for doc in docs if len(doc) == 2]
            return docs
    except:
        return []

def save_list(obj, path):
    with open(path, 'w', encoding='utf-8') as f:
        for row in obj:
            f.write('{}\n'.format(row))

def save_json(json_obj, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(json_obj, f, ensure_ascii=False, indent=2)

def save_list_of_json(json_list, path, op='w'):
    with open(path, op, encoding='utf-8') as f:
        for obj in json_list:
            obj_strf = json.dumps(obj, ensure_ascii=False)
            f.write('{}\n'.format(obj_strf))

def load_reviews(path):
    with open(path, encoding='utf-8') as f:
        reviews = [line.strip() for line in f]
    reviews = [json.loads(r) for r in reviews if r]
    return reviews

if __name__ == '__main__':
    main()
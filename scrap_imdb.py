import argparse
import json
import os

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

    args = parser.parse_args()
    directory = args.directory
    begin_year = args.begin_year
    end_year = args.end_year
    scrap_main = args.scrap_main
    scrap_credits = args.scrap_credits
    scrap_keywords = args.scrap_keywords
    scrap_quotes = args.scrap_quotes
    scrap_reviews = args.scrap_reviews
    debug = args.debug

    # check output directory
    directories = ['{}/main/', '{}/credits/', '{}/keywords/', '{}/quotes/', '{}/reviews/']
    if not os.path.exists(directory):
        os.makedirs(directory)

    print('Scrap main    : {}'.format(scrap_main))
    print('Scrap credits : {}'.format(scrap_credits))
    print('Scrap keywords: {}'.format(scrap_keywords))
    print('Scrap quotes  : {}'.format(scrap_quotes))
    print('Scrap reviews : {}'.format(scrap_reviews))
    print('year          : {} ~ {}'.format(begin_year, end_year))

    for year in range(begin_year, end_year - 1, -1):

        id_list_path = 'movie_lists/{}.txt'.format(year)
        if not os.path.exists(id_list_path):
            print('List of {} year does not exist'.format(year))
            continue

        title_idxs = load_movie_idx(id_list_path)
        if debug:
            title_idxs = title_idxs[:10]

        # TODO

        print('done year = {}'.format(year))

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

if __name__ == '__main__':
    main()
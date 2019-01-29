import argparse
import json
import os
from imdb_scraper import yield_topmovie_title_idxs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str, default='./movie_lists', help='Output directory')
    parser.add_argument('--begin_year', type=int, default=1930, help='yyyy form')
    parser.add_argument('--end_year', type=int, default=2019, help='yyyy form')
    parser.add_argument('--sleep', type=float, default=2.0, help='yyyy form')
    parser.add_argument('--max_num', type=int, default=1500, help='Maximum number of movies for each year')

    args = parser.parse_args()
    directory = args.directory
    begin_year = args.begin_year
    end_year = args.end_year
    max_num = args.max_num
    sleep = args.sleep

    if not os.path.exists(directory):
        os.makedirs(directory)

    for year in range(end_year, begin_year - 1, -1):
        path = '{}/{}.txt'.format(directory, year)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write('title\tidx\n')
                for tidxs in yield_topmovie_title_idxs(year, max_num, sleep, verbose=True):
                    for title, idx in tidxs:
                        title = title.replace('\t', ' ').replace('\n', ' ').replace('\r', '')
                        f.write('{}\t{}\n'.format(title, idx))
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()

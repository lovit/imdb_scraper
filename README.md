# IMDb scraper


## Usage

### Scrap meta data

영화 아이언맨의 meta data 수집을 위해 `parse_main` 함수를 이용합니다.

```python
from imdb_scraper import parse_main

idx = 371746
parse_main(idx)
```

```
{'Also Known As': 'Iron man - El hombre de hierro',
 'Alternate Versions': 's The scene where Stark reads a newspaper with the headline "Who Is the Iron Man?" differs on the theatrical and DVD/Blu-ray releases. On the theatrical release, the newspaper used a spy photo of Iron Man, which was taken by freelance photographer Ronnie Adams during the film\'s production on May 2007. When Adams learned that his picture was used in the film, he filed a lawsuit against Paramount Pictures and Marvel Studios for using the picture without permission. As a result, the newspaper was altered to show a different picture of Iron Man on the DVD/Blu-ray release.',
 'Aspect Ratio': '2.39 1',
 'Budget': '$140,000,000 (estimated)',
 'Certificate': ['12', 'See all certifications'],
 'Color': 'Color',
 'Country': 'USA',
 'Crazy Credits': 's Part of the closing credits are seen against computer-graphic renders of armoured suits. One of the renders is an armour with a Gatling gun attached - the War Machine suit, which would appear in Iron Man 2 (2010).',
 'Cumulative Worldwide Gross': '$585,174,222, 2 October 2008',
 'Directors': [{'id': 269463, 'name': 'Jon Favreau'}],
 'Filming Locations': 'Palmdale Regional Airport, Palmdale, California, USA',
 'Genres': ['Action', 'Adventure', 'Sci-Fi'],
 'Goofs': 's (at around 4 mins) Stark is said to have graduated from MIT summa cum laude, but MIT does not graduate people with honors.',
 'Gross USA': '$318,412,101, 2 October 2008',
 'Language': ['English', 'Persian', 'Urdu', 'Arabic', 'Hungarian'],
 'Official Sites': ['Official Facebook', 'Official site'],
 'Opening Weekend USA': '$98,618,668, 2 May 2008, Wide Release',
 'Parents Guide': 'View content advisory',
 'Plot Keywords': ['robot suit',
  'based on comic',
  'billionaire',
  'inventor',
  'stan lee character'],
 'Production Co': 'Paramount Pictures, Marvel Enterprises, Marvel Studios',
 'Release Date': '30 April 2008 (South Korea)',
 'Runtime': '126 min',
 'Sound Mix': ['SDDS', 'Dolby Digital', 'DTS'],
 'Taglines': 'Get ready for a different breed of heavy metal hero.',
 'Title': 'Iron Man (2008)',
 'Trivia': 'a This is the last film special effects expert Stan Winston completed before his death.',
 'Year': '2008'}
```


### Scrap credits

영화 아이언맨에 출연한 배우 목록을 가져오기 위하여 `parse_credits` 을 이용합니다.

```python
from imdb_scraper import parse_credits

parse_credits(idx)
```

```
{'name': 'Robert Downey Jr.', 'id': 375, 'role': 'Tony Stark / Iron Man', 'order': 1}
{'name': 'Terrence Howard', 'id': 5024, 'role': 'Rhodey', 'order': 2}
{'name': 'Jeff Bridges', 'id': 313, 'role': 'Obadiah Stane', 'order': 3}
{'name': 'Gwyneth Paltrow', 'id': 569, 'role': 'Pepper Potts', 'order': 4}
{'name': 'Leslie Bibb', 'id': 4753, 'role': 'Christine Everhart', 'order': 5}
{'name': 'Shaun Toub', 'id': 869467, 'role': 'Yinsen', 'order': 6}
{'name': 'Faran Tahir', 'id': 846687, 'role': 'Raza', 'order': 7}
...
```


### Scrap reviews

영화 아이언맨의 리뷰를 가져오려면 `yield_reviews` 를 이용합니다. 서버로부터 리뷰를 받을 때마다 list of dict 형식의 reviews 를 yield 합니다.

```python
from pprint import pprint
from imdb_scraper import yield_reviews

idx = 371746
for reviews in yield_reviews(idx, max_page=3):
    pprint(reviews[0])
```

```
{'content': 'Amazing. Just amazing. The MCU started off with a bang. Robert '
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
 'user': 'ur98135771'}
```

### Scrap keywords

영화 아이언맨의 키워드를 가져오려면 `pasrse_keywords` 를 이용합니다.

```python
from imdb_scraper import parse_keywords

parse_keywords(idx)
```

```
['robot suit',
 'based on comic',
 'billionaire',
 'inventor',
 'stan lee character',
 'high tech',
 'marvel cinematic universe',
 'playboy',
 'armor',
 'genius',
 'engineer',
 ...]
```

### Scrap quotes

영화의 극중 명대사를 수집하려면 `parse_quotes` 를 이용합니다.

```python
from imdb_scraper import parse_quotes

parse_quotes(idx)
```

```
[{'agree': '116 of 116', 'character': 'Tony Stark', 'quote': 'I am Iron Man.'},
 {'agree': '92 of 93', 'character': 'Yinsen', 'quote': "So you're a man who has everything... and nothing."},
 {'agree': '59 of 59', 'character': 'Tony Stark', 'quote': "[reading the newspaper] Iron Man. That's kind ..."},
 {'agree': '55 of 55', 'character': '', 'quote': '[dies]'},
 {'agree': '47 of 47', 'character': 'Tony Stark', 'quote': "Please don't follow me ..."},
 {'agree': '38 of 38', 'character': 'Tony Stark', 'quote': "I shouldn't be alive... unless it ..."},
 ...]
```

### Scrap top movies per each year

매 년, 인기 순으로 top k 개의 영화의 제목과 id 를 가져옵니다.

```python
from imdb_scraper import yield_topmovie_title_idxs

for tidxs in yield_topmovie_title_idxs(2018, max_num=100):
    # do something
    for (title, idx) in tidxs:
        print((title, idx))
```

```
('Bohemian Rhapsody', 1727824)
('The Favourite', 5083738)
('Roma', 6155172)
('Aquaman', 1477834)
('A Star Is Born', 1517451)
('Green Book', 6966692)
('Vice', 6266538)
('Bird Box', 2737304)
('Spider-Man: Into the Spider-Verse', 4633694)
('Bumblebee', 4701182)
...
```

### Scrap script

다섯 가지 항목에 대하여 scripts 를 이용하여 한 번에 수집 가능합니다. 서버에 과도한 부하를 주지 않기 위하여 multiprocessing 은 지원하지 않습니다.

`movie_lists` 폴더에 연도 별 영화의 제목과 아이디가 저장된 `year.txt`  파일이 있다고 가정합니다.

| Argument | Type | Default | Help |
| --- | --- | --- | --- |
| directory | str | './output' | Output directory |
| begin_year | int | 1930 | yyyy form |
| end_year | int | 2019 | yyyy form |
| sleep | float | 10.0 | yyyy form |
| main | Boolean | False | action='store_true' |
| credits | Boolean | False | action='store_true' |
| keywords | Boolean | False | action='store_true' |
| quotes | Boolean | False | action='store_true' |
| reviews | Boolean | False | action='store_true' |
| debug | Boolean | False | 매년 10 개의 영화만 scraping |
| rescrap | Boolean | False | 이미 scrap 한 리뷰라도 re-scrap. Rescrap 시 이전에 수집한 데이터는 제거. False 일 경우, 이전에 수집하지 않은 리뷰만 추가로 수집 |
| start-movie-index | int | 0 | end_year 의 영화 리스트 내 영화 중 scrap 을 하지 않는 영화 개수 |

```
python scrap_imdb.py --begin_year 2017 --end_year 2018 --debug --main --credits --keywords --reviews --quotes
```

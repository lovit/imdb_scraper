# IMDb scraper


## Usage

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
{'name': 'Clark Gregg', 'id': 163988, 'role': 'Agent Coulson', 'order': 8}
{'name': 'Bill Smitrovich', 'id': 810488, 'role': 'General Gabriel', 'order': 9}
{'name': 'Sayed Badreya', 'id': 46223, 'role': 'Abu Bakaar', 'order': 10}
{'name': 'Paul Bettany', 'id': 79273, 'role': 'JARVIS (voice)', 'order': 11}
{'name': 'Jon Favreau', 'id': 269463, 'role': 'Hogan', 'order': 12}
{'name': 'Peter Billingsley', 'id': 82526, 'role': 'William Ginter Riva', 'order': 13}
{'name': 'Tim Guinee', 'id': 347375, 'role': 'Major Allen', 'order': 14}
{'name': 'Will Lyman', 'id': 528164, 'role': 'Award Ceremony Narrator (voice)', 'order': 15}
{'name': 'Tom Morello', 'id': 603780, 'role': 'Guard', 'order': 16}
{'name': 'Marco Khan', 'id': 434879, 'role': 'Guard', 'order': 17}
{'name': 'Daston Kalili', 'id': 435771, 'role': 'Guard', 'order': 18}
{'name': 'Ido Mor', 'id': 2789241, 'role': 'Guard (as Ido Ezra)', 'order': 19}
{'name': 'Kevin Foster', 'id': 1080555, 'role': 'Jimmy', 'order': 20}
...
```
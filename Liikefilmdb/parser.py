import requests
from bs4 import BeautifulSoup
import re
from .movie import Movie


class Parser:
  data = None
  logger = None
  url = ''

  def __init__(self, _logging, _URI):
    self.logger = _logging
    self.url = _URI
    

  def get_data(self, url):
    #TODO: customize user agent, add headers, cookies, etc
    try:
        response = requests.get(url)
        data = response.text
        return data
    #TODO: handle specific exceptions
    except Exception as ex:
       self.logger.exception(ex)
  
  def get_movies(self, data):
    r = re.compile("uiStandartVarListWidth*")
    bs = BeautifulSoup(data,"lxml")
    movies = bs.find_all('div', {'class': 'uiMovieListSimpleSection'})
    return movies
  
  def set_stars_count(self, movie):
    stars_count = 1
    stars_block = movie.div.find('div', {'class': 'uiMovieVarXVTitle'}).div.find_all('i')
    for s in stars_block:
        if ('#daa520' in s.attrs['style']):
            stars_count+=1
    return stars_count
  
  def handle_description(self, val):
      return val.find_all('p')[0].text.strip()
  
  def get_movies_info(self, html_page):
    movies = self.get_movies(html_page)
    movies_info = []
    for m in movies:
      i = self.handle_movie(m)
      movies_info.append(i)
    return movies_info

#TODO: finish prasing
  def handle_movie(self, movie):
      try:
        r = re.compile('uiStandartVarList')
        m = Movie()
        m.set_id(movie.attrs['id'])
        m.set_name(movie.div.find('div', {'class': 'uiMovieVarXVTitle'}).text.strip())
        #m.set_stars_raiting(self.set_stars_count(movies[0]))
        rev_block = movie.div.find('table', {'class': r})
        for tr in rev_block.find_all('tr'):
            divName = tr.find('td', {'class': 'uiStandartVarListName'})
            divVal = tr.find_all('td', {'class': 'uiStandartVarListVal'})
            if (divName.text.strip() == 'Оценка'):
              m.set_imdb_kp_raitings(divVal[0])
            if (divName.text.strip() == 'Жанр'):
              m.set_genre(divVal[0])
            if (divName.text.strip() == 'Страна'):
              m.set_country(divVal[0])
            if (divName.text.strip() == 'В главных ролях'):
              m.set_actors(divVal[0])
            if (divName.text.strip() == 'Режиссёр'):
              m.set_director(divVal[0])
            if (divName.text.strip() == 'Длительность'):
              m.set_duration(divVal[0])
        desc = self.handle_description(movie)
        m.set_description(desc)
      except Exception as ex:
        #TODO: change to logger via print
        print("exception hannepd while try to handle movie {} {}".format(movie, ex))
      return m
  
  def get_links(self, html_page):
    links = []
    bs = BeautifulSoup(html_page,"lxml")
    links_div = bs.find_all('div', {'class': 'uiMainV3ListWrapper_element'})
    for link in links_div:
      href = link.find('a').get('href')
      links.append(href)
    return links
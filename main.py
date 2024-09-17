
from Liikefilmdb import LikeFilmDbDriver, Parser
import logging
import sys
from pprint import pprint
import pickle

URI = "https://likefilmdb.ru"

if __name__ == "__main__":
  logging.basicConfig(stream=sys.stdout, level=logging.INFO)
  driver = LikeFilmDbDriver(logging)
  parser = Parser(logging, URI)
  
  #GET LINKS FROM HTML PAGE. REMOVE AFTER END PARSER
  links_page = driver.get_html_page(URI)
  links = parser.get_links(links_page)
  all_movies = []
  logging.info("get all links for parsing")
  for link in links:
    logging.info("start handle link {}".format(link))
    page_movies = driver.get_all_movies(URI + link)
    logging.info("getted movies from link {} {}".format(link, len(page_movies)))
    with open('/home/ser_evegenii/stuff/machine_learning/movies_recomendations/data/{}'.format(link.replace("/",'_')), 'wb') as file:
      pickle.dump(page_movies, file)
    for m in page_movies:
      logging.info("start handle movie from parsed link")
      parsed_movies = parser.get_movies_info(m)
      all_movies.append(parsed_movies)
  with open('/home/ser_evegenii/stuff/machine_learning/movies_recomendations/pparsed_data.pkl', 'wb') as file:
    pickle.dump(all_movies, file)



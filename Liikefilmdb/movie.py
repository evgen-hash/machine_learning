import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import json

class Movie:
    id = 0
    name = ''
    desription = ''
    duration = ''
    director = []
    actors = []
    country = []
    genre = []
    grade = ''
    imdb_raiting = 0
    kp_raiting = 0
    stars_raitinig = 0
    
    def set_id(self, _id):
        self.id = _id
    def set_name(self, _name):
        self.name = _name
    def set_description(self, _description):
        self.description = _description
    def set_duration(self, val):
        self.duration = val.text

    def set_director(self, val):
        self.director = val.text.split(',')
    def set_actors(self, val):
        self.actors = val.text.split(',')
    def set_country(self, val):
        self.country = val.text.split(',')
    def set_genre(self, val):
        self.genre = val.text.split(',')
    def set_grade(self, _grade):
        self.grade = _grade
    def set_imdb_kp_raitings(self, val):
        try:
          _,self.imdb_val,_,self.kp_val = val.text.split(' ')
        except Exception as ex:
          print("dont have some value in {}".format(val))
    def set_imdb_raiting(self, _imdb):
        self.imdb = _imdb
    def set_kp_raiting(self, _kp):
        self.kp = _kp
    def set_stars_raiting(self, _stars):
        self.stars = _stars

    def print_fields(self):
        print("####")
        print(self.__dict__)
        print("#######")

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)
    


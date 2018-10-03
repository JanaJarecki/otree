from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'dfe'
    players_per_group = None
    num_rounds = 2
    expectedvalues = [0, 100]

class Subsession(BaseSubsession):
  pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
  rnd = models.FloatField(initial = -999)
  choice = models.IntegerField()
  def draw_choice(self):
     self.rnd = random.gauss(Constants.expectedvalues[self.choice], 1)
  pass

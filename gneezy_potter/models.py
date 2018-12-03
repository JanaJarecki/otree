from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import numpy


author = 'Jana B. Jarecki'

doc = """
Risk preference elicitation task by Gneezy & Potter (1997).
"""


class Constants(BaseConstants):
    name_in_url = 'gneezy_potter'
    players_per_group = None
    num_rounds = 1
    lang = 'de'

def make_field(label):
  return models.IntegerField(
    label = label,
    min = 0,
    max = 100
  )

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
  riskGneezyPotter = make_field('67% earn zero or 33% earn 2.5 times the amount.')

  def get_bonus(self):
    self.payoff = (100 - self.riskGneezyPotter + numpy.random.binomial(n = 1, p = 0.33) * 2.5 * self.riskGneezyPotter) / 10
  pass

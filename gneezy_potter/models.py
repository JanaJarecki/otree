from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Jana B. Jarecki'

doc = """
Risk preference elicitation task by Gneezy & Potter (1997).
"""


class Constants(BaseConstants):
    name_in_url = 'gneezy_potter'
    players_per_group = None
    num_rounds = 1

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
  riskGneezyPotter = make_field('67% earn zero or 33% earn 2.5X.')
  pass
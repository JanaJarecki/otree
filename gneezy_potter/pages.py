from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class GneezyPotter(Page):
  form_model = 'player'
  form_fields = ['riskGneezyPotter']
  pass

page_sequence = [
    GneezyPotter
]

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class GneezyPotter(Page):
  form_model = 'player'
  form_fields = ['riskGneezyPotter']
  def before_next_page(self):
    self.player.get_bonus()
  pass


page_sequence = [
    GneezyPotter
]

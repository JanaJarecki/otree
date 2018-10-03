from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass

class Consent(Page):
  pass

class SelectDomain(Page):
  def is_displayed(self):
    return ((self.round_number-1) % 26) == 0
  form_model = "player"
  form_fields = ["selectedDomain"]
  def vars_for_template(self):
    return {
      "domains": list( zip(
        [ "risk_domains/" + d + ".jpg" for d in self.player.get_available_domains() ],
        [ self.player.get_domain_labels(d) for d in self.player.get_available_domains() ],
        self.player.get_available_domains() ) )
    }
  pass

class FamiliarizeDomain(Page):
  def is_displayed(self):
    return ((self.round_number-1) % 26) == 0
  def vars_for_template(self):
    return self.player.vars_for_template()
  pass

class Choice(Page):
  def is_displayed(self):
    return self.player.round_number <= (10 * 27)
  form_model: "player"
  form_fields: ["f1", "f2", "f3", "choice"]
  def vars_for_template(self):
    context = self.player.vars_for_template()
    context.update({
      "features": self.player.participant.vars['features']
    })
    return context


class JudgeDomain(Page):
  def is_displayed(self):
    return self.round_number <= (10 * 27)
  form_model = "player"
  form_fields = ["risk", "benefit"]
  pass


page_sequence = [
    SelectDomain,
    FamiliarizeDomain,
    Choice
]

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Prolificid(Page):
  form_model = 'player'
  form_fields = ['prolificid']
  def is_displayed(self):
    return self.round_number == 1


class Consent(Page):
  def is_displayed(self):
    return self.round_number == 1

  def vars_for_template(self):
    return {
    'participation_fee': self.participant.payoff_plus_participation_fee(),
    }


class Coverstory(Page):
  def is_displayed(self):
    return self.round_number == 1


class Coverstory_check(Page):
  def is_displayed(self):
    return self.round_number == 1


class Incentives(Page):
  def is_displayed(self):
    return self.round_number == 1

  def vars_for_template(self):
    return {
    'participation_fee': self.participant.payoff_plus_participation_fee(),
    'real_world_currency_per_point': c(1).to_real_world_currency(self.session),
    'example_pay': c(12).to_real_world_currency(self.session)
    }


class ResultsWaitPage(WaitPage):
  def after_all_players_arrive(self):
    for p in self.subsession.get_players():
      if self.round_number > 1:
        p.successes = p.get_last_success()
        if (not self.subsession.is_new_block()) & self.subsession.is_multitrial():
            p.state = p.get_last_state()


class NewBlock(Page):
  def is_displayed(self):
    return (self.subsession.is_new_block() & self.subsession.is_multitrial())

  def vars_for_template(self):
    context =  self.player.vars_for_template()
    context.update({
      'currentblock': self.player.block,
      'budget': self.player.budget,
      'num_blocks': self.session.vars['num_blocks'],
      'successes': self.player.get_last_success(),
      'successes': self.player.get_last_success()})
    return context

class Choices(Page):
  form_model = 'player'

  def is_displayed(self):
    return self.round_number <= Constants.num_multitrial

  def get_form_fields(self):
    choicefields = ['choice{}'.format(i) for i in range(1, Constants.num_trials + 1)]
    statefields = ['state{}'.format(i) for i in range(1, Constants.num_trials + 2)]
    rtfields = ['rt_ms{}'.format(i) for i in range(1, Constants.num_trials + 1)]
    return choicefields + statefields + rtfields + ['success'] + ['successes']

  def vars_for_template(self):
    context =  self.player.vars_for_template()
    context.update({
      'outcomes': self.participant.vars['outcomes'][self.player.block],
      'successes': self.player.get_last_success()})
    return context

  def before_next_page(self):
    if self.round_number == Constants.num_multitrial:
      self.player.draw_bonus()
  # def before_next_page(self):
  #   if self.round_number <= Constants.num_multitrial:
  #     self.player.get_outcome()
    # self.player.update_successes()

class InstructionOneshot(Page):
  def is_displayed(self):
    return self.round_number == Constants.num_multitrial + 1

class ChoicesOneShot(Page):
  form_model = 'player'
  def is_displayed(self):
    return self.round_number > Constants.num_multitrial

  def get_form_fields(self):
    choicefields = ['choice' +str(int(self.player.trial))]
    statefields = ['state' +str(int(self.player.trial))]
    rtfields = ['rt_ms' +str(int(self.player.trial))]
    return choicefields + statefields + rtfields

  def vars_for_template(self):
    return self.player.vars_for_template()

  # def before_next_page(self):
  #     self.player.get_outcome()
  #     self.player.update_successes()


class Results(Page):
  def is_displayed(self):
    return self.round_number <= Constants.num_multitrial

  def vars_for_template(self):
    maxx = max(map(max, *self.participant.vars['actions'][self.player.block]))
    max_earnings = max(maxx * Constants.num_trials, self.player.budget + .01)
    p = self.player
    return {
      'state': p.state + p.outcome,
      'required': p.budget - p.state,
      'budget': p.budget,
      'trial': p.trial,
      'max_less_state': max_earnings - p.state,
      'max_earning': max_earnings,
      'num_blocks': self.session.vars['num_blocks'],
      'successes': p.successes
      }


class Payment(Page):
  def is_displayed(self):
    return self.round_number >= Constants.num_rounds

  def vars_for_template(self):
    return {
      'participation_fee': c(self.session.config['participation_fee']).to_real_world_currency(self.session),
      # 'bonus': c(self.player.bonus).to_real_world_currency(self.session),
      'bonus': c(self.player.draw_bonus()).to_real_world_currency(self.session)
      }

# class ChoicesUncover(Page):

#   def is_displayed(self):
#     return self.round_number == 5
#   form_model = 'player'
#   form_fields = ['choice']
#   def vars_for_template(self):
#     return {
#       'HV': self.participant.vars['outcomes'][1],
#       'HP': self.participant.vars['probabilities'][1],
#       'LV': self.participant.vars['outcomes'][0],
#       'LP': self.participant.vars['probabilities'][0],
#       'state': sum([p.state for p in self.player.in_all_rounds()]),
#       'budget': self.player.budget,
#       'choice': self.player.choice,
#       'chart_trial': [1] * (self.participant.vars['trial'] + 1),
#       'max_less_state': int(max(self.participant.vars['outcomes'][1])) * Constants.num_rounds - sum([p.outcome for p in self.player.in_all_rounds()]),
#       'max_earning': int(max(self.participant.vars['outcomes'][1])) * Constants.num_rounds
#       }


page_sequence = [
  Prolificid,
  # Consent,
  # Coverstory,
  # #Coverstory_check,
  # #Incentives,
  # NewBlock,
  # Choices,
  InstructionOneshot,
  ChoicesOneShot
  ]

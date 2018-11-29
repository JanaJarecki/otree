from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import math
import numpy
import csv
from django.utils.translation import ugettext as _
from . import exp

author = 'Jana B. Jarecki'

doc = """
Risk sensitive foraging
"""

PM = exp.pm
AM = exp.am

class Constants(BaseConstants):
  name_in_url = 'rsf'
  players_per_group = None
  num_familiarization_rounds = 1
  num_repetitions = 9 * 2
  num_trials = 5
  num_multitrial = num_repetitions + num_familiarization_rounds
  num_oneshot = 21 * 2
  num_rounds = PM.num_rounds
  point_label = _('Punkte')
  trial_label = _('Entscheidung')
  action_label = _('Option')
  initial_state = 0
  num_actions = 2
  lang = 'eng'


class Subsession(BaseSubsession):
  def concat_stimulus(self, i, stimuli):
    y = "_".join( str(x) for x in ['%.0f' % stimuli[i][0], '%.0f' % (stimuli[i][2] * 100), '%.0f' % stimuli[i][1]] )
    return(y)

  def creating_session(self):
  # Executed at the very start, loops through each num_trial
    for p in self.get_players():
      round_number = self.round_number
      phase_number = PM.get_phaseN(round_number)
      phase = PM.get_phaseL(round_number)
      stimuli = AM.get_stimuli(round_number, phase_number)
      stimulus_position = AM.get_action_position(round_number)
      feature_color = AM.get_feature_appearance(round_number)[0]

      # Store variables
      p.phase = PM.get_phaseL(round_number)
      p.block = PM.get_block(round_number)      
      p.budget = stimuli[2][0]
      p.stimulus0 = self.concat_stimulus(0, stimuli)
      p.stimulus1 = self.concat_stimulus(1, stimuli)
      if (phase in ['critical']):
        p.state = stimuli[2][1]
        p.trial = stimuli[2][2]
      else:
        p.state = Constants.initial_state
        p.trial = 1
      p.successes = 0

      # Do and store the randomizations
      p.layout_featurecolor = '_'.join(''.join(str(y) for y in x) for x in [feature_color])     
      p.layout_stimulusposition_01 = ''.join(str(x) for x in stimulus_position)

      # Initialize containers
      n = int(Constants.num_rounds + 1)
      if (self.round_number == 1):
        self.session.vars['instruction_rounds'] = PM.get_instruction_rounds()
        print(self.session.vars['instruction_rounds'])
        p.participant.vars['stimulus_position'] = [None] * n
        p.participant.vars['img1'] = [None] * n
        p.participant.vars['img2'] = [None] * n
        p.participant.vars['max_earnings'] = [None] * n
        p.participant.vars['num_blocks'] = [None] * n
        p.participant.vars['outcomes'] = [None] * n
      p.participant.vars['stimulus_position'][round_number] = stimulus_position
      css_img_orig_position = [
        'sprite_' + p.stimulus0 + '_featurecolor' + p.layout_featurecolor,
        'sprite_' + p.stimulus1 + '_featurecolor' + p.layout_featurecolor
          ]
      p.participant.vars['img1'][round_number] = css_img_orig_position[stimulus_position[0]]
      p.participant.vars['img2'][round_number] = css_img_orig_position[stimulus_position[1]]
      if (phase in ['familiarize', 'training']):
        outcomes_orig_position = [p.draw_outcomes(x, Constants.num_trials) for x in AM.get_stimuli(round_number, phase_number)[ :2]]
        p.participant.vars['outcomes'][round_number] = [outcomes_orig_position[i] for i in stimulus_position]
      maxx = max([max(stimuli[i]) for i in [0,1]])
      p.participant.vars['max_earnings'][round_number] = max(maxx * (Constants.num_trials), p.budget)
      p.participant.vars['num_blocks'][round_number] = PM.get_num_trials_in_phase(round_number)

      if (self.round_number == 1):
        p.state = Constants.initial_state
        p.successes = 0
          
        # p.budget = p.participant.vars['budgets'][p.block]
        # p.set_xp(p.participant.vars['actions'][p.block])
        # p.colorx1_x2 = random.randint(0, 1)

          
          # #rnd_environments = numpy.array(rnd_environments)
          # p.participant.vars['actions'] = rnd_actions       
          # p.participant.vars['budgets'] = numpy.array([x[2][0] for x in rnd_environments])
          # self.session.vars['num_actions'] = Constants.num_actions
          # self.session.vars['num_blocks'] = PM.blocks[PM.i]

          # # Predefine random outcomes of all options in all trials
          # p.participant.vars['outcomes'] = [ [ p.draw_outcomes(gamble, PM.trials[PM.i] + 1) for gamble in a] for a in rnd_actions]
          
          


      # if (self.round_number > 1) & self.is_multitrial():
      #   for p in self.get_players():
      #     # At the start of each new trial
      #     lastp = p.in_round(self.round_number - 1)
      #     p.trial = lastp.trial + 1
      #     p.block = lastp.block
      #     p.budget = lastp.budget
      #     p.colorx1_x2 = lastp.colorx1_x2
      #     p.set_xp(p.participant.vars['actions'][p.block])

      #     if self.is_new_block():
      #       # At the start of a new block
      #       p.block = lastp.block + 1
      #       p.trial = 1
      #       p.state = Constants.initial_state
      #       p.colorx1_x2 = 1 - lastp.colorx1_x2
      #       p.budget = p.participant.vars['budgets'][p.block]
      #       p.set_xp(p.participant.vars['actions'][p.block])

      # if (self.round_number - 1) == Constants.num_multitrial:
      #   critical_trials = self.load_choice_environment('risk_sensitive_foraging/critical_trials.csv')

      #   for p in self.get_players():
      #     rnd_critical_trials = self.randomize_row_order(critical_trials)
      #     rnd_critical_actions = self.randomize_col_order(rnd_critical_trials, 0, Constants.num_actions)
      #     rnd_critical_trials = numpy.array(rnd_critical_trials)

      #     p.participant.vars['actions_cr'] = rnd_critical_actions       
      #     p.participant.vars['budgets_cr'] = [x[2][0] for x in rnd_critical_trials]
      #     p.participant.vars['states_cr'] = [x[2][1] for x in rnd_critical_trials]
      #     p.participant.vars['trials_cr'] = [x[2][2] for x in rnd_critical_trials]
      #     self.session.vars['num_blocks_cr'] = len(critical_trials)

      #     # Initial values for critical trials
      #     p.block = 0
      #     p.trial = p.participant.vars['trials_cr'][p.block]
      #     p.state = p.participant.vars['states_cr'][p.block]
      #     p.budget = p.participant.vars['budgets_cr'][p.block]
      #     p.set_xp(p.participant.vars['actions_cr'][p.block])
      #     p.colorx1_x2 = random.randint(0, 1)

      # if (self.round_number - 1) > Constants.num_multitrial:
      #   for p in self.get_players():  
      #     lastp   = p.in_round(self.round_number - 1)
      #     p.block = lastp.block + 1
      #     p.trial = p.participant.vars['trials_cr'][p.block]
      #     p.state = p.participant.vars['states_cr'][p.block]
      #     p.budget = p.participant.vars['budgets_cr'][p.block]
      #     p.colorx1_x2 = 1 - lastp.colorx1_x2
      #     p.set_xp(p.participant.vars['actions_cr'][p.block])
  # def is_new_block(self):
  #   round_number = self.round_number
  #   if (round_number == 1):
  #     return(False)
  #   else:
  #     return((PM.get_block(round_number - 1) != PM.get_block(round_number)))


  # def is_multitrial(self):
  #   xx = (self.round_number - 1) < Constants.num_multitrial
  #   return xx



class Group(BaseGroup):
  pass


def make_choice_field(trial):
  return models.IntegerField(
    doc = "Chosen stimulus in trial" +str(trial) +", this is the stimulus, not the shown stimulus position")

def make_state_field(trial):
  return models.IntegerField(
    doc = "Point state at the beginning of trial" +str(trial))

def make_rt_field(trial):
  return models.FloatField(
    doc = "Reaction time  in ms from the end of the page load until the choice, in trial" +str(trial) +" or until submit, in case of instruction pages.")

# Every round the playder object is re-initialized
class Player(BasePlayer):
  prolificid = models.StringField(
    doc = "ID of the survey provider")
  browser = models.StringField(
    doc = "Browser and version", blank=True)
  phase = models.StringField(
    doc = "Phases during the experiment. Familiarization phase is not incentivized. Training phase is incentivized and has 5 trials per block. Test phase is incentivized and has 1 trial per block")
  block = models.IntegerField(
    doc = "Current block")
  trial = models.FloatField(
    doc = "Current trial of 5")
  stimulus0 = models.StringField(
    doc = "Risky gamble number one, format x1_p1_x2.")
  stimulus1 = models.StringField(
    doc = "Risky gamble number two, format x1_p2_x2.")
  state = models.FloatField(
    doc = "Accumulated points before the current decision")
  budget = models.FloatField(
    doc = "Earnings requirement in current block")
  choice1 = make_choice_field(1)
  choice2 = make_choice_field(2)
  choice3 = make_choice_field(3)
  choice4 = make_choice_field(4)
  choice5 = make_choice_field(5)
  state1  = make_state_field(1)
  state2  = make_state_field(2)
  state3  = make_state_field(3)
  state4  = make_state_field(4)
  state5  = make_state_field(5)
  state6  = make_state_field(6)
  rt_ms1 = make_rt_field(1)
  rt_ms2 = make_rt_field(1)
  rt_ms3 = make_rt_field(1)
  rt_ms4 = make_rt_field(1)
  rt_ms5 = make_rt_field(1)
  success = models.IntegerField(doc = "Indicator if in the current block the earnings requirement (budget) was reached, 1 if yes, 0 otherwise")
  # outcome = models.IntegerField(doc = "Randomly drawn outcome of the chosen option given the choice in this trial")
  successes = models.FloatField(initial = 0, doc = "Count of the total number of blocks where the earnings requirement (budget) was reached")
  rt_ms = models.FloatField(
    doc = "Reaction time from the end of the page load until the choice or until submit, in case of instruction pages.")
  layout_featurecolor = models.StringField(
    doc = "Layout: Randomized feature colors per trial (light vs dark grey), 01 means that in this trial feature x1 was light grey and feature x2 dark grey, 10 denotes that x1 was dark grey.")
  layout_stimulusposition_01 = models.StringField(
    doc = "Layout: Randomized stimulus position per trial (left vs right), 01 if stimulus1 was left, 10 if stimulus1 was right.")
  # left_x1 = models.FloatField(doc = "Outcome 1 of the option that was shown on the left (option position was randomized across participants)")
  # left_x2 = models.FloatField(doc = "Outcome 2 of the option that was shown on the left (option position was randomized across participants)")
  # left_p1 = models.FloatField(doc = "Probability of outcome 1 of the option that was shown on the left (option position was randomized across participants)")
  # left_p2 = models.FloatField(doc = "Probability of outcome 2 of the option that was shown on the left (option position was randomized across participants)")
  # right_x1 = models.FloatField(doc = "Outcome 1 of the option that was shown on the right (option position was randomized across participants)")
  # right_x2 = models.FloatField(doc = "Outcome 2 of the option that was shown on the right (option position was randomized across participants)")
  # right_p1 = models.FloatField(doc = "Probability of outcome 1 of the option that was shown on the right (option position was randomized across participants)")
  # right_p2 = models.FloatField(doc = "Probability of outcome 2 of the option that was shown on the right (option position was randomized across participants)")

  # def set_xp(self, actions):
  #   self.option1 = "_".join( str(x) for x in [action[0][i] for i in [0,2,1]] )
  #   self.option2 = "_".join( str(x) for x in [action[1][i] for i in [0,2,1]] )

  def draw_outcomes(self, action, size):
    p = action[2: ][1]
    indices = numpy.random.binomial(n=1, p=p, size=size)
    #indices = [0, 1, 0, 1, 1, 0, 1, 0, 1, 1]
    x = action[ :2]
    res = [x[i] for i in indices]
    return res

  # def get_outcome(self):
  #   self.outcome = self.participant.vars['outcomes'][self.block][self.choice][self.trial]

  def get_last_state(self):
    if (self.round_number > 1):
      lastself = self.in_round(self.round_number - 1)
      return lastself.state + lastself.outcome
    else:
      return self.state

  def update_successes(self):
    n_ignore = Constants.num_familiarization_rounds
    successes = 0
    if (self.round_number >  n_ignore):
      successes = sum([p.success for p in self.in_rounds(n_ignore + 1, self.round_number - 1)])
      self.successes = successes
    return(successes)
    
  
  def get_last_success(self):
    round_num_ignore = 1 + Constants.num_familiarization_rounds
    if (self.round_number > round_num_ignore):
      return self.in_round(self.round_number - 1).success
    else:
      return 0


  def vars_for_template(self):
    n = self.round_number
    # act = 'actions'
    # nb = 'num_blocks'
    # block = self.block
    # round_number = self.round_number
    # if self.round_number > Constants.num_multitrial:
    #    act += '_cr'
    #    nb += '_cr' 
    # x1 = [ str(int(x)) for x in self.participant.vars[act][block][0][ :2]]
    # p1 = [ str(int(100 * x)) for x in self.participant.vars[act][block][0][2: ]]
    # x2 = [ str(int(x)) for x in self.participant.vars[act][block][1][ :2]]
    # p2 = [ str(int(100 * x)) for x in self.participant.vars[act][block][1][2: ]]
    return {
      'img1': self.participant.vars['img1'][n],
      'img2': self.participant.vars['img2'][n],
      'stimulus_position': self.participant.vars['stimulus_position'][n],
      'state': self.state,
      'budget': self.budget,
      'trial': self.trial,
      'max_earning': self.participant.vars['max_earnings'][n],
      'max_less_state': self.participant.vars['max_earnings'][n] - 0,
      'num_blocks': self.participant.vars['num_blocks'][n], #todo add this by phase
      'multitrial': self.phase in ['familiarize', 'training']
    }

  def draw_bonus(self):
    bonus_rounds = PM.get_bonus_rounds()
    self.payoff = sum([ self.terminal_reward(i) for i in bonus_rounds])
    return self.payoff

  def terminal_reward(self, i):
    p = self.in_round(i)
    return p.success * p.state6



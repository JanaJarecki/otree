import numpy as np
import csv
import random

phases  = ['familiarize', 'training', 'critical']
"""Names of the different phases"""
stimuli = [1, 9, 46]
"""How many unique stimuli are there in each phase?"""
blocks  = [1, 7, 1]
"""How many blocks are there in each phase?"""
trials  = [1, 1, 1]
"""How many trials are there PER BLOCK in each phase?"""

bonus_trials = [None]
"""Trials that are randomly drawn for the bonus"""
bonus_blocks = [None]
"""How many blocks are drawn for the bonus in each phase?"""
bonus_trials = [0, 1, 0]
"""How many blocks are drawn for the bonus in each phase?"""

counts_from_one = 1
"""NOT IMPLEMENTED. 1 if trials and block counts should start at 1, 0 otherwise"""

f = 'risk_sensitive_foraging/static/risk_sensitive_foraging/stimuli/'
filepaths = [f + 'familiarization.csv',
            f + 'learning.csv',
            f +  'critical.csv']
"""Relative path to location where the stimuli are stored, one per phase."""

numactions = [2, 2, 2]
"""How many actions/options are available per filepath"""

numfeatures = [[2, 2],
               [2, 2],
               [2, 2]]
"""How many features do the actions/options have per filepath?"""

randomize_feature = ['appearance/trial'] #['appearance/once']
"""List with strings what to randomize in features
   '' = no randomization
   'appearance/once'
   'appearance/block'
   'appearance/trial'
   'position/once'
   'position/trial'
   'position/block'
"""
randomize_action = ['position/trial']
"""List with strings what to randomize in features
   'color/once'
   'color/phase'
   'color/block'
   'color/trial'
   'position/once'
   'position/phase'
   'position/block'
   'position/trial'
"""

randomize_stimulus_order = 'block'
"""String containing how to randomize randomize in features
   '' = No randomization
   'once'
   'phase'
   'block'
"""

num_rounds = sum([a * b * c for a, b, c in zip(stimuli, blocks, trials)])

class Phasemanager:
  def __init__(self, phases, stimuli, blocks, trials):
    self.doc = "Manage phases object holding the phases"
    self.num_rounds_per_phase = [a * b * c for a, b, c in zip(stimuli, blocks, trials)]
    self.num_rounds = sum(self.num_rounds_per_phase)
    self.phases = phases
    self.stimuli = stimuli
    self.blocks = blocks
    self.trials = trials
    round_number = range(self.num_rounds)
    phaseN = range(len(phases))
    self.trials_per_phase = [a * b * c for a, b, c in zip(stimuli, blocks, trials)]
    phase_number = np.repeat(phaseN, self.trials_per_phase)
    tmp = [item for sublist in [range(x) for x in blocks] for item in sublist] 
    block_number = []
    for a, b in zip(tmp, np.repeat(stimuli,blocks)):
      block_number.extend([a] * b)
    tmp = [range(x) for x in stimuli]
    stimulus_number = [item for sublist in np.repeat(tmp, blocks) for item in sublist]
    decision_number = [range(x) for x in self.trials_per_phase]
    decision_number = [item for sublist in decision_number for item in sublist]
    bonus_in_block = [random.sample(range(self.trials_per_phase[i]), k = bonus_trials[i]) for i in phaseN]
    is_bonus_trial = [[False] * i for i in self.trials_per_phase]
    for i in phaseN:
      for j in bonus_in_block[i]:
        is_bonus_trial[i][j] = True
    self.is_bonus_trial = [i for sublist in is_bonus_trial for i in sublist]
    lookup = np.column_stack((round_number, phase_number, block_number, stimulus_number, decision_number))
    self.lookup = lookup
  def get_phaseN(self, round_number):
    return(self.lookup[round_number-1, 1])
  def get_phaseL(self, round_number):
    return(phases[self.get_phaseN(round_number)])
  def get_block(self, round_number):
    return(self.lookup[round_number-1, 2] + counts_from_one)
  def get_stimulus(self, round_number):
    return(self.lookup[round_number-1, 3])
  def get_num_trials_in_phase(self, round_number):
    return(self.trials_per_phase[self.get_phaseN(round_number)])
  def get_bonus_rounds(self):
    return(self.lookup[self.is_bonus_trial, 0] + 1)
  def get_instruction_rounds(self):
    return([i + 1 for i in np.cumsum(self.trials_per_phase)])
  def get_decision_number_in_phase(self, round_number):
    return(self.lookup[round_number-1, 4] + counts_from_one)

def load_choice_environment(filepath):
  with open(filepath) as csvfile:
    next(csvfile)
    file = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    environment = [[row[ :4], row[4:8], row[8: ]] for row in file]
  return environment

# def randomize_row_order(self, x):
#   # x is the list with environments
#   # first environment is a test environment
#   copy = x[1:]
#   random.shuffle(copy) # Random order
#   x[1:] = copy # overwrite the original
#   return x

# def randomize_col_order(self, x, first, last):
#   # x is the environment, first, last is the row index of the actions
#   x = [y[ first : last ] for y in x]
#   for a in x:
#     random.shuffle(a)
#   return x

class Appearancemanager:
  def __init__(self, PM, filepaths, numfeatures, numactions, randomize_feature, randomize_action, randomize_stimulus_order):
    # Load the environment
    self.environments = [load_choice_environment(x) for x in filepaths]
    # Randomizations
    # Stimuli: Display order of the stimuli
    self.stimulus_order = np.repeat([range(x) for x in PM.stimuli], PM.blocks)
    if (randomize_stimulus_order == 'block'):
      self.stimulus_order = [random.sample(x, k=len(x)) for x in self.stimulus_order]   
    self.stimulus_order = [item for sublist in self.stimulus_order for item in sublist]
    # Action: Position of the action buttons (stimuli) or keys
    # tmp = [a * b * c  for a, b, c in zip(PM.stimuli, PM.trials, PM.blocks)]
    num_rounds_per_phase = PM.num_rounds_per_phase
    print(num_rounds_per_phase)
    num_rounds = PM.num_rounds
    num_phases = len(PM.phases)
    print(num_rounds)
    self.action_positions = [list(range(x)) for x in np.repeat(numactions, num_rounds_per_phase)]
    if ('position/trial' in randomize_action):
      self.action_positions = [random.sample(x, k=len(x)) for x in self.action_positions]
    # Determine position and appearance of features ---------------------------
    numactions_long = np.repeat(numactions, num_rounds_per_phase)
    numfeatures_long = [[numfeatures[i]] * num_rounds_per_phase[i] for i in range(num_phases)]
    numfeatures_long = [item for sublist in numfeatures_long for item in sublist] # this is just to flatten it to one vector
    self.feature_appearances = [[list(range(numfeatures_long[i][0]))] * numactions_long[i] for i in range(num_rounds)] # todo: this only works if feature.0 and feature.1 have the same number of values
    if ('appearance/trial' in randomize_feature):
      self.feature_appearances = [[random.sample(range(numfeatures_long[i][0]), k = numfeatures_long[i][0])] * numactions_long[i] for i in range(num_rounds)]
    print(self.feature_appearances)
    print(self.action_positions)
  def get_stimuli(self, round_number, phase_number):
    i = self.stimulus_order[round_number-1]
    return(self.environments[phase_number][i])
  def get_action_position(self, round_number):
    return(self.action_positions[round_number-1])
  def get_feature_appearance(self, round_number):
    return(self.feature_appearances[round_number-1])

    # # Randomize what is shown when and where
    # rnd_environments = self.randomize_row_order(environments)
    # #rnd_environments = environments # todo: TAKE THIS OUT
    # rnd_actions = self.randomize_col_order(rnd_environments, 0, Constants.num_actions)

    # # Randomize what is shown when and where
    # rnd_environments = self.randomize_row_order(environments)
    # #rnd_environments = environments # todo: TAKE THIS OUT
    # rnd_actions = self.randomize_col_order(rnd_environments, 0, Constants.num_actions)






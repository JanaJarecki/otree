from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


author = 'Jana B. Jarecki'

doc = """
Risk taking in domains
"""


class Constants(BaseConstants):
    name_in_url = 'risk_domains'
    players_per_group = None
    num_rounds = 10 * 27
    features = [
    [0, 0 ,0],
    [0, 0 ,1],
    [0, 0 ,2],
    [0, 1 ,0],
    [0, 1 ,1],
    [0, 1 ,2],
    [0, 2 ,0],
    [0, 2 ,1],
    [0, 2 ,2],
    [1, 0 ,0],
    [1, 0 ,1],
    [1, 0 ,2],
    [1, 1 ,0],
    [1, 1 ,1],
    [1, 1 ,2],
    [1, 2 ,0],
    [1, 2 ,1],
    [1, 2 ,2],
    [2, 0 ,0],
    [2, 0 ,1],
    [2, 0 ,2],
    [2, 1 ,0],
    [2, 1 ,1],
    [2, 1 ,2],
    [2, 2 ,0],
    [2, 2 ,1],
    [2, 2 ,2]
    ]

class Subsession(BaseSubsession):
  def creating_session(self):
    if ((self.round_number == 1) | (self.round_number % 27 == 0)):
      for p in self.get_players():
        p.participant.vars['features'] = p.randomize_row_order(Constants.features)
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
  selectedDomain = models.StringField()
  f1 = models.IntegerField()
  f2 = models.IntegerField()
  f3 = models.IntegerField()
  choice = models.IntegerField()

  def vars_for_template(self):
    if (self.round_number - 1) % 26 == 0:
      dom = self.selectedDomain
      self.participant.vars["selectedDomain"] = dom
    else:
      dom = self.participant.vars["selectedDomain"]
    return {
      "domain": self.selectedDomain,
      "domain_label": self.get_domain_labels(dom),
      "domain_description": self.get_domain_description(dom),
      "domain_img": "risk_domains/" +dom + ".jpg",
      "domain_attributes": self.get_domain_attributes(dom),
      "attribute_value_labels": [ self.get_domain_value_labels(dom, j) for j in self.get_domain_attributes(dom) ],
      "domain_question": self.get_domain_question(dom)
    }

  def randomize_row_order(self, x):
    rnd_x = x.copy()
    random.shuffle(rnd_x) # Random order
    return rnd_x
  def get_attribute_values(self, i):
    f1 = Constants.features[i][0]
    f2 = Constants.features[i][1]
    f3 = Constants.features[i][2]
    return Constants.features[i]
  def get_available_domains(self):
    if self.round_number == 1:
      return ["bgc", "wgc", "fac", "fse", "mat", "mre", "env", "sta", "kin", "par"]
    else:
      return list(set(["bgc", "wgc", "fac", "fse", "mat", "mre", "env", "sta", "kin", "par"]) - set([p.selectedDomain for p in self.in_previous_rounds()]))
  def get_domain_labels(self, i):
    if i == "bgc":
      return "Team goals"
    if i == "wgc":
      return "Personal goals"
    if i == "env":
      return "Travel + Nature"
    if i == "sta":
      return "Respect + Status"
    if i == "fse":
      return "Groceries"
    if i == "fac":
      return "Eating + Drinking"
    if i == "mat":
      return "Flirting"
    if i == "mre":
      return "Love + Relationship"
    if i == "kin":
      return "Helping Family"
    if i == "par":
      return "Help by parents"
  def get_domain_description(self, i):
    if i == "bgc":
      return [ "involves situations where you consider yourself a member of a team and the team competes with another group.", "Think of team sports, political parties, competing work teams, or school group assignments."]
    if i == "wgc":
      return [ "involves situations where your own goals conflict with the goals of your peers or friends.", "For example, going to your favorite place for dinner that your friends don't like that much, selling more than your colleagues for a bonus, becoming the leader in your work team."]
    if i == "sta":
      return [ "involves situations in which you have to act because other people may challenge your social status.", "Think of calling out people that failed to respect you, engaging in open confrontations to avoid losing face, or betraying one person to gain or keep another person's trust."]
    if i == "env":
      return [ "involves situations where you explore the world or new parts of nature.", "Think of travels to far away locations, outdoor activities like mountain hiking, or wildwater rafting, or a safari."]
    if i == "fse":
      return [ "involves situations where you can buy high-quality groceries.", "Think of discount or expensive products, growing your own food, farmer's markets, sustainable food."]
    if i == "fac":
      return [ "involves you eating or drinking habits.", "Think of eating at restaurants of varying hygene standards, eating something beyong expiration date, not washing vegetables before eating them, etc."]
    if i == "par":
      return [ "involves situations in which you may need to ask your parents for something.", "Think of asking for financial support, an old item of your parents, to stay with them rent-free, to help pay a debt."]
    if i == "kin":
      return [ "involves situations where you may do things that are important for your family but not necessarily for you.", "Think of spending time with sick relatives, donating money to relatives, helping relatives out, risking something for the safety of a relative."]
    if i == "mat":
      return [ "involves situations in which you decide what to do during flirtation.", "Think of casual flirts, having casual sex, trying out new things, commitment to be exclusive."]
    if i == "mre":
      return [ "involves situations where you can make an investment in an existing romantic relationship.", "Think of taking an early relationship to a serious level, not flirting with others while in a relationship, cheating on a partner, showing love and affection during a fight, spending money and time for a partner."]
  def get_domain_attributes(self, i):
    if i == "bgc":
      return["Other team is aggressive", "Other team is friendly", "Size of the other team"]
    if i == "wgc":
      return [ "Importance of goal to you", "Your skills reaching the goal", "Competitor skills reaching the goal" ]
    if i == "sta":
      return [ "Involved people are aggressive", "Own action violates norms", "Involved people initiated it" ]
    if i == "env":
      return [ "Area involves natural hazards", "Other people join the trip", "Trip has a goal" ]
    if i == "fse":
      return [ "Your financial situation", "Food is expensive", "Food has health benefits" ]
    if i == "fac":
      return [ "Your hunger level", "Place seems dirty", "Food seems clean" ]
    if i == "par":
      return [ "Parents' help is useful for you", "Parent's financial situation", "Your financial situation" ]
    if i == "kin":
      return [ "Your costs of helping", "Helping solves their problem", "Family member and you are close" ]
    if i == "mat":
      return [ "Your interest in a relationship", "Date interested in a relationship", "Your peers learn about it" ]
    if i == "mre":
      return [ "Partner previously hurt you", "Your interest in relationship", "Your behavior hurts partner" ]
  def get_domain_value_labels(self, i, j):
    if (i == "bgc") & (j == "Size of the other group"):
      return ["very small", "equal", "very large"]
    if (i == "fse") & (j == "Your financial situation"):
      return ["limited funds", "average", "well funded"]
    if (i == "par") & (j != "Parents' help is useful for you"):
      return ["limited funds", "average", "well funded"]
    else:
      return ["not much", "medium", "very much"]
  def get_domain_question(self, i):
    if i == "bgc":
      return "Would you say something impolite to a person in the competitor team"
    if i == "wgc":
      return "Would you try to steer others toward your ideas"
    if i == "sta":
      return "Would you blackmail another person to win a competition"
    if i == "env":
      return "Would you do a trip to an area with landslide risks"
    if i == "fse":
      return "Would you buy relatively expensive organic food"
    if i == "fac":
      return "Would you eat something that has fallen on the floor"
    if i == "par":
      return "Would you ask for financial help from your parents"
    if i == "kin":
      return "Would you help your sibling athough you are short on time"
    if i == "mat":
      return "Would you have unprotected sex"
    if i == "mre":
      return "Would you get physical with another person that is not your romatic partner"

  
  pass

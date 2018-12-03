from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age',
                   'gender',
                   'income',
                   'language_english']

class OpenQuestions(Page):
    form_model = 'player'
    form_fields = ['task_clear',
                   'strategy',
                   'dataquality',
                   'open_text'
                   ]


# class CognitiveReflectionTest(Page):
#     form_model = 'player'
#     form_fields = ['crt_bat',
#                    'crt_widget',
#                    'crt_lake']


page_sequence = [
    Demographics,
    OpenQuestions
]

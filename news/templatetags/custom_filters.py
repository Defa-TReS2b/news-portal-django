from django import template
import re

register = template.Library()

REPLACEMENT_WORDS = ['редиска', 'деятельности', 'историю']

@register.filter()
def censor(value):
    outcome = value
    for word in REPLACEMENT_WORDS:
        outcome = re.sub(word, word[0] + "*" * (len(word) - 1), outcome, flags=re.IGNORECASE)
    return outcome

from django.test import TestCase

import os
from polls.models import Question, Choice


#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# Create your tests here.
q = Question.objects.get(pk=1)
q.choice_set.create(choice_text='Not much', votes=0)
q.choice_set.create(choice_text='The sky', votes=0)
c = q.choice_set.create(choice_text='Just hacking again', votes=0)

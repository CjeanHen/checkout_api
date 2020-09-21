from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Answer(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields
  response = models.CharField(max_length=500)
  created_on = models.DateField(auto_now_add=True)
  author = models.CharField(max_length=500, blank=True)
  owner = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
  )
  answer_to = models.ForeignKey(
    'Question',
    related_name = 'answers',
    on_delete = models.CASCADE
  )
  on_survey = models.ForeignKey(
    'Survey',
    related_name = 'responses',
    on_delete = models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"{self.response} "

  def as_dict(self):
    """Returns dictionary version of Mango models"""
    return {
        'id': self.id,
        'created_on': self.created_on,
        'response': self.response,
        'owner': self.owner
    }

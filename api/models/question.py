from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Question(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields
  question = models.CharField(max_length=200)
  created_on = models.DateField(auto_now_add=True)
  owner = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
  )
  part_of = models.ForeignKey(
    'Survey',
    related_name = 'questions',
    on_delete = models.CASCADE
  )
  def __str__(self):
    # This must return a string
    return f"{self.question} "

  def as_dict(self):
    """Returns dictionary version of Mango models"""
    return {
        'id': self.id,
        'created_on': self.created_on,
        'question': self.question,
        'owner': self.owner
    }

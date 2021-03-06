from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Survey(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=300)
  created_on = models.DateField(auto_now_add=True)
  author = models.CharField(max_length=500, blank=True)
  owner = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"{self.name} {self.description}"

  def as_dict(self):
    """Returns dictionary version of Mango models"""
    return {
        'id': self.id,
        'created_on': self.name,
        'questions': self.questions,
        'owner': self.owner
    }

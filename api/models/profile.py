from django.db import models
from django.contrib.auth import get_user_model

# Model for the profile of the user
class Profile(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  bio = models.TextField()
  # photo = models.ImageField()
  surveys = models.ForeignKey(
    'Survey',
    related_name='surveys',
    on_delete=models.CASCADE
  )
  owner = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"{self.first_name} {self.last_name}"

  def as_dict(self):
    """Returns dictionary version of Mango models"""
    return {
        'id': self.id,
        'first_name': self.first_name,
        'bio': self.bio,
        'surveys': self.surveys,
        'owner': self.owner
    }

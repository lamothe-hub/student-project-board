from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    body = models.TextField()
    skills = models.TextField()
    university = models.CharField(max_length = 100)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]

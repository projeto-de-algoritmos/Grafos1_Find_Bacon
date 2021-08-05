from django.db import models

# Create your models here.
class Graph(models.Model):
    json_graph = models.JSONField()

class Search(models.Model):
    search_text = models.CharField(max_length=250)
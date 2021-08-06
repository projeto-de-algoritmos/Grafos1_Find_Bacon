from django.db import models

class Graph(models.Model):
    json_graph = models.JSONField()

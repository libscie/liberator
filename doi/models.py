from django.db import models
from django.contrib.postgres.fields import JSONField

class Article(models.Model):
    doi_prefix = models.CharField(max_length=255)
    doi_suffix = models.CharField(max_length=255)
    crossref = JSONField()
    zenodo_deposit = JSONField()
    has_been_uploaded = models.BooleanField(default=False)
    free_fulltext_url = models.URLField(blank=True)

class PDF(models.Model):
    file = models.FileField()
    article = models.ForeignKey('Article')

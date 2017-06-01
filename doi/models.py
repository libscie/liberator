from django.db import models
from django.contrib.postgres.fields import JSONField

class Article(models.Model):
    doi_prefix = models.CharField(max_length=255)
    doi_suffix = models.CharField(max_length=255)
    crossref = JSONField(default={})
    oadoi = JSONField(default={})
    zenodo = JSONField(default={})
    has_been_uploaded = models.BooleanField(default=False)
    free_fulltext_url = models.URLField(blank=True)

    def __str__(self):
        return self.doi_prefix + '/' + self.doi_suffix

    class Meta:
        unique_together = [('doi_prefix', 'doi_suffix')]

class PDF(models.Model):
    file = models.FileField()
    article = models.ForeignKey('Article')

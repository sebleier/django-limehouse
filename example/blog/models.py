from django.db import models


class Entry(models.Model):
    title = models.CharField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=80)

    def __unicode__(self):
        return self.title
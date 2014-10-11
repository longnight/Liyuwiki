from django.db import models
import secretballot
import time, datetime
import os


def content_file_name(instance, filename):
    fileExtension = os.path.splitext(filename)[1].lower()
    head = datetime.datetime.now().strftime("%Y_%m") + "/"
    tail = '_'.join(['liyuwiki_com', str(int(time.time()))]) + fileExtension
    return head + tail


class Terms(models.Model):
    term = models.CharField(max_length=30, unique=True)
    uid = models.PositiveIntegerField(blank=True, unique=True)
    term_pinyin = models.CharField(max_length=250)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(default='1984-06-04')
    visit_times = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.term


class Definitions(models.Model):
    Terms = models.ForeignKey(Terms, related_name='terms_definitions')
    definition = models.TextField(max_length=200, blank=False)
    author = models.CharField(max_length=65, blank=True)
    homepage = models.URLField(max_length=200, blank=True)
    author_email = models.EmailField(blank=True)
    vote_rank = models.SmallIntegerField(default=0)
    vote_rank2 = models.FloatField(default=0.0)
    show = models.BooleanField(default=False)
    uid = models.PositiveIntegerField(blank=True, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    docfile = models.ImageField(upload_to=content_file_name, blank=True, null=True)

    def __unicode__(self):
        return self.definition

secretballot.enable_voting_on(Definitions)



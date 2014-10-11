#coding=utf-8

from wikidict.models import *
from wikidict.views import *
from wikidict.forms import *
from wikidict.script import *



t = Terms.objects.all()
d = Definitions.objects.all()
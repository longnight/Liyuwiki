#coding=utf-8
import datetime
from haystack import indexes
from models import Definitions


class DefIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')
    created_time = indexes.DateTimeField(model_attr='created_time')

    def get_model(self):
        return Definitions

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
        # return self.get_model().objects.filter(created_time__lte=datetime.datetime.now()).filter(show=True)
# -*- coding: utf-8 -*-
from haystack import indexes
from blog.models import Note
# 修改此处，类名为模型类的名称+Index，比如模型类为Note,则这里类名为NoteIndex
class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    def get_model(self):
        # 修改此处，为你自己的model
        return Note
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
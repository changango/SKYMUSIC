# 定义索引类
from haystack import indexes
# 导入数据模型
from index.models import songs


class songsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return songs

    # 建立索引的数据
    def index_queryset(self, using=None):
        return self.get_model().objects.all()



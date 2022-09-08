from django.shortcuts import render
from haystack.views import SearchView
from index.models import dynamic


class MySearchView(SearchView):

    def create_response(self):
        context = self.get_context()
        for i in context['page']:
            res = dynamic.objects.get(song_id=i.object.songs_id)
            res.search += 1
            res.save()

        return render(self.request, self.template, context)

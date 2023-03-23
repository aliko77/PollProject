# from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from apps.poll.models import Poll


# Create your views here.

class ListPublicPool(ListView):
    model = Poll
    template_name = "public_poll/list.html"
    context_object_name = 'polls'
    queryset = Poll.objects.filter(is_active=True, is_private=False)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_value = self.request.GET.get("search")
        if search_value:
            queryset = queryset.filter(
                Q(title__icontains=search_value) |
                Q(description__icontains=search_value) |
                Q(tags__icontains=search_value)
            )
        return queryset

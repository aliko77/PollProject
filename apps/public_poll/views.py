# from django.shortcuts import render
from django.views.generic import ListView

from apps.poll.models import Poll


# Create your views here.

class ListPublicPool(ListView):
    model = Poll
    template_name = "public_poll/list.html"
    context_object_name = 'polls'
    queryset = Poll.objects.filter(is_active=True, is_private=False)

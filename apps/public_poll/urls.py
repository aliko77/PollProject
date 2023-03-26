from django.urls import path
from .views import ListPublicPoll, VotePublicPoll, VotePublicPollWithInvite

urlpatterns = [
    path("", ListPublicPoll.as_view(), name="poll.public.list"),
    path("v/<slug:poll_slug>", VotePublicPoll.as_view(), name="poll.public.vote"),
    path("i/<str:invite_link>", VotePublicPollWithInvite.as_view(), name="poll.public.vote.invite")
]

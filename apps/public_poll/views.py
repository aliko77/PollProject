# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from apps.poll.models import Poll, PollInviteLinks, PollVote
from .models import PollResolved


# Create your views here.

def ispollready(poll, invite_link=None):
    if not poll.is_active:
        return False
    if poll.is_private:
        if not invite_link:
            return False
        else:
            is_exist = poll.pollinvitelinks_set.get(link=invite_link)
            if not is_exist:
                return False
    questions = poll.pollquestion_set.filter(is_active=True)
    if questions.count() == 0:
        return False
    return True


def render_vote_html(request, template_name, poll_object):
    return render(request, template_name, {
        "poll": poll_object,
        "questions": poll_object.pollquestion_set.order_by("id"),
        "cho_list": ("text", "number", "date", "email", "time")
    })


class ListPublicPoll(ListView):
    model = Poll
    template_name = "public_poll/list.html"
    context_object_name = 'polls'
    queryset = Poll.objects.filter(is_active=True, is_private=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["resolved_list"] = PollResolved.objects. \
                filter(user=self.request.user).values_list("poll_id", flat=True)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(~Q(pollresolved__user__in=[self.request.user]))
        search_value = self.request.GET.get("search")
        if search_value:
            queryset = queryset.filter(
                Q(title__icontains=search_value) |
                Q(description__icontains=search_value) |
                Q(tags__icontains=search_value)
            )
        return queryset


class VotePublicPoll(LoginRequiredMixin, View):
    template_name = "public_poll/vote.html"

    def get(self, request, poll_slug):
        poll_object = get_object_or_404(Poll, slug=poll_slug)
        if not ispollready(poll_object):
            return redirect("poll.public.list")
        return render_vote_html(request, self.template_name, poll_object)

    @staticmethod
    def post(request, **kwargs):
        return SubmitPublicPoll(request).post()


class VotePublicPollWithInvite(View):
    template_name = "public_poll/vote.html"

    def get(self, request, invite_link):
        invite_object = get_object_or_404(PollInviteLinks, link=invite_link)
        poll_object = get_object_or_404(Poll, pk=invite_object.poll.pk)
        if not ispollready(poll_object, invite_link):
            return redirect("poll.public.list")
        return render_vote_html(request, self.template_name, poll_object)

    @staticmethod
    def post(request, **kwargs):
        return HttpResponse(SubmitPublicPoll(request).post())


class SubmitPublicPoll:
    def __init__(self, request):
        self.request = request

    def post(self):
        items = self.request.POST
        lists = self.request.POST.lists()
        item_poll_identy = items.get("poll_identy")
        poll_object = get_object_or_404(Poll, id=item_poll_identy)
        if not ispollready(poll_object):
            return redirect("poll.public.list")
        for key, values in lists:
            if key.startswith("Q_"):
                question_id = key.rsplit("_", 1)[-1]
                PollVote(
                    user=self.request.user,
                    poll=poll_object,
                    question_id=question_id,
                    answer_id=None,
                    content=values if len(values) > 1 else values[0]
                ).save()
        PollResolved(
            user=self.request.user,
            poll=poll_object
        ).save()
        return HttpResponse(True)

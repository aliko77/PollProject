# from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from django.db.models import Q
from apps.poll.models import Poll, PollInviteLinks


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
    answers = poll.pollanswer_set.filter(is_active=True)
    if questions.count() == 0 or (answers.count() < questions.count()):
        return False
    return True


def render_vote_html(request, template_name, poll_object):
    return render(request, template_name,
        {
            "poll"     : poll_object,
            "questions": poll_object.pollquestion_set.order_by("id"),
            "cho_list" : ("text", "number", "date", "email", "time")
        }
    )


class ListPublicPoll(ListView):
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


class VotePublicPoll(View):
    template_name = "public_poll/vote.html"

    def get(self, request, poll_slug):
        poll_object = get_object_or_404(Poll, slug=poll_slug)
        if not ispollready(poll_object):
            return redirect("poll.public.list")
        return render_vote_html(request, self.template_name, poll_object)


class VotePublicPollWithInvite(View):
    template_name = "public_poll/vote.html"

    def get(self, request, invite_link):
        invite_object = get_object_or_404(PollInviteLinks, link=invite_link)
        poll_object = get_object_or_404(Poll, pk=invite_object.poll.pk)
        if not ispollready(poll_object, invite_link):
            return redirect("poll.public.list")
        return render_vote_html(request, self.template_name, poll_object)

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import DeleteView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
import datetime
from .models import Poll, PollQuestion, PollAnswer, PollQuestionChoices, PollInviteLinks
from .forms import CreatePollForm, CreatePollQuestionForm, CreatePollAnswerForm


# Create your views here.

class ListPoll(LoginRequiredMixin, ListView):
    model = Poll
    template_name = "poll/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_polls"] = self.model.objects.filter(
            author=self.request.user
        )
        return context


class CreatePoll(LoginRequiredMixin, View):
    template_name = "poll/create.html"

    def post(self, request):
        form = CreatePollForm(request.POST)
        if not form.is_valid():
            messages.error(
                request=request, message='Bir hata oluştu.'
            )
            return render(request, self.template_name)
        try:
            b_is_active = True if request.POST.get("is_active") == "on" else False
            b_is_private = True if request.POST.get("is_private") == "on" else False
            b_tags = request.POST.get("tags").strip().replace(" ", "")
            b_starts_at = datetime.datetime.now() if b_is_active else None
            cp = Poll(
                author=request.user,
                title=request.POST.get("title"),
                description=request.POST.get("description"),
                meta_title=b_tags,
                tags=b_tags,
                starts_at=b_starts_at,
                is_active=b_is_active,
                is_private=b_is_private
            )
            cp.save()
            messages.success(self.request, "Başarıyla eklendi.")
            return redirect("poll.update", pk=cp.id)
        except ValueError:
            messages.error(
                request=request, message='Bir hata oluştu.'
            )
            return redirect(self.template_name)

    def get(self, request):
        return render(request, self.template_name)


class UpdatePoll(LoginRequiredMixin, View):
    template_name = "poll/update.html"

    def get(self, request, pk):
        poll_object = get_object_or_404(Poll, pk=pk, author=self.request.user)
        return render(request, self.template_name, {"poll": poll_object})

    def post(self, request, pk):
        form = CreatePollForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Form geçersiz.")
            return HttpResponseRedirect(self.request.path_info)
        try:
            poll_object = get_object_or_404(Poll, pk=pk, author=self.request.user)
            poll_object.title = request.POST.get("title")
            poll_object.description = request.POST.get("description")
            poll_object.tags = request.POST.get("tags").strip().replace(" ", "")
            poll_object.is_active = True if request.POST.get("is_active") == "on" else False
            poll_object.is_private = True if request.POST.get("is_private") == "on" else False
            poll_object.save()
            messages.success(request, "Başarıyla düzenlendi.")
        except ValueError:
            messages.error(request, "Bir hata oluştu.")
        return HttpResponseRedirect(self.request.path_info)


class DeletePoll(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Poll
    success_url = reverse_lazy('poll.index')
    success_message = "Başarıyla silindi."

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class CreatePollQuestion(LoginRequiredMixin, View):
    template_name = "poll/question/create.html"

    def get(self, request, poll_id):
        poll_object = get_object_or_404(Poll, pk=poll_id, author=self.request.user)
        questions = poll_object.pollquestion_set.all()
        return render(request, self.template_name,
            {"questions": questions, "poll": poll_object, "type_choices": PollQuestionChoices.get_choices()}
        )

    def post(self, request, poll_id):
        form = CreatePollQuestionForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Form geçersiz.")
            return HttpResponseRedirect(self.request.path_info)
        try:
            poll_object = get_object_or_404(Poll, pk=poll_id, author=self.request.user)
            cpq = PollQuestion(
                type=request.POST.get("type"),
                content=request.POST.get("content"),
                meta=request.POST.get("meta"),
                is_active=True if request.POST.get("is_active") == "on" else False,
                poll=poll_object
            )
            cpq.save()
            messages.success(request, "Başarıyla eklendi.")
        except ValueError:
            messages.error(request, "Bir hata oluştu.")
        return HttpResponseRedirect(self.request.path_info)


class UpdatePollQuestion(LoginRequiredMixin, View):
    template_name = "poll/question/update.html"

    def get(self, request, pk, poll_id):
        poll_object = get_object_or_404(Poll, pk=poll_id, author=self.request.user)
        question_object = get_object_or_404(PollQuestion, pk=pk, poll_id=poll_object.id)
        return render(request, self.template_name,
            {"question": question_object, "type_choices": PollQuestionChoices.get_choices()}
        )

    def post(self, request, pk, poll_id):
        form = CreatePollQuestionForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Form geçersiz.")
            return HttpResponseRedirect(self.request.path_info)
        try:
            poll_object = get_object_or_404(Poll, pk=poll_id, author=self.request.user)
            question_object = get_object_or_404(PollQuestion, pk=pk, poll_id=poll_object.id)
            question_object.content = request.POST.get("content")
            question_object.meta = request.POST.get("meta")
            question_object.type = request.POST.get("type")
            question_object.is_active = True if request.POST.get("is_active") == "on" else False
            question_object.save()
            messages.success(request, "Başarıyla düzenlendi.")
        except ValueError:
            messages.error(request, "Bir hata oluştu.")
        return HttpResponseRedirect(self.request.path_info)


class DeletePollQuestion(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PollQuestion
    success_message = "Başarıyla silindi."

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def get_success_url(self):
        return reverse_lazy('poll.question.create', kwargs={"poll_id": self.object.poll.id})


class CreatePollAnswer(LoginRequiredMixin, View):
    template_name = "poll/answer/create.html"

    def get(self, request, poll_id, question_id):
        poll_object = get_object_or_404(Poll, pk=poll_id, author=self.request.user)
        question_object = get_object_or_404(PollQuestion, pk=question_id, poll_id=poll_object.id)
        question_answers = question_object.pollanswer_set.all()
        return render(request, self.template_name, {"answers": question_answers, "question": question_object})

    def post(self, request, poll_id, question_id):
        form = CreatePollAnswerForm(request.POST)
        if not form.is_valid():
            messages.error(self.request, "Form geçersiz.")
            return HttpResponseRedirect(self.request.path_info)
        try:
            poll_object = get_object_or_404(Poll, pk=poll_id, author=self.request.user)
            question_object = get_object_or_404(PollQuestion, pk=question_id, poll_id=poll_object.id)
            cpa = PollAnswer(
                content=request.POST.get("content"),
                meta= PollAnswer.set_meta_data(request.POST.get("meta")),
                is_active=True if request.POST.get("is_active") else False,
                question=question_object,
                poll=poll_object
            )
            cpa.save()
            messages.success(self.request, "Başarıyla eklendi.")
        except ValueError:
            messages.error(self.request, "Bir hata oluştu.")
        return HttpResponseRedirect(self.request.path_info)


class UpdatePollAnswer(LoginRequiredMixin, View):
    template_name = "poll/answer/update.html"

    def get(self, request, poll_id, question_id, pk):
        poll_object = get_object_or_404(Poll, pk=poll_id, author=self.request.user)
        answer_object = get_object_or_404(PollAnswer, pk=pk, poll_id=poll_object.id, question_id=question_id)
        return render(request, self.template_name, {"answer": answer_object})

    def post(self, request, poll_id, question_id, pk):
        form = CreatePollAnswerForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Form geçersiz.")
            return HttpResponseRedirect(self.request.path_info)
        try:
            poll_object = get_object_or_404(Poll, pk=poll_id, author=self.request.user)
            answer_object = get_object_or_404(PollAnswer, pk=pk, poll_id=poll_object.id, question_id=question_id)
            answer_object.content = request.POST.get("content")
            answer_object.meta = request.POST.get("meta")
            answer_object.is_active = True if request.POST.get("is_active") else False
            answer_object.save()
            messages.success(request, "Başarıyla düzenlendi.")
        except ValueError:
            messages.error(request, "Bir hata oluştu.")
        return HttpResponseRedirect(self.request.path_info)


class DeletePollAnswer(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PollAnswer
    success_message = "Başarıyla silindi."

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def get_success_url(self):
        return reverse_lazy('poll.answer.create',
            kwargs={"poll_id": self.object.poll.id, "question_id": self.object.question.id}
        )


class CreatePollInviteLink(LoginRequiredMixin, View):
    template_name = "poll/update.html"

    def post(self, request, poll_id):
        poll_object = get_object_or_404(Poll, pk=poll_id, author=self.request.user)
        if poll_object.pollinvitelinks_set.count() >= 10:
            messages.error(self.request, "Maksimum 10 adet davet linki oluşturabilirsin.")
            return render(request, self.template_name, {"poll": poll_object})
        else:
            try:
                pil = PollInviteLinks(
                    amount=0,
                    usage=0,
                    author=self.request.user,
                    poll=poll_object
                )
                pil.save()
                messages.success(self.request, "Başarıyla eklendi.")
            except ValueError:
                messages.error(self.request, "Bir hata oluştu.")
        return render(request, self.template_name, {"poll": poll_object})


class DeletePollInviteLink(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PollInviteLinks
    success_message = "Başarıyla silindi."

    def test_func(self):
        obj = self.get_object()
        return obj.poll.author == self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def get_success_url(self):
        return reverse_lazy('poll.update',
            kwargs={"pk": self.object.poll.id}
        )

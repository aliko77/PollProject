from django.urls import path
from .views import \
    ListPoll, CreatePoll, UpdatePoll, DeletePoll, \
    CreatePollQuestion, UpdatePollQuestion, DeletePollQuestion, \
    CreatePollAnswer, UpdatePollAnswer, DeletePollAnswer

urlpatterns = [
    path("index", ListPoll.as_view(), name="poll.index"),
    path("create", CreatePoll.as_view(), name="poll.create"),
    path("<int:pk>/edit", UpdatePoll.as_view(), name="poll.update"),
    path("<int:pk>/delete", DeletePoll.as_view(), name="poll.delete"),
    # PollQuestion"
    path("<int:poll_id>/question/create", CreatePollQuestion.as_view(), name="poll.question.create"),
    path("<int:poll_id>/question/<int:pk>/update", UpdatePollQuestion.as_view(), name="poll.question.update"),
    path("<int:poll_id>/question/<int:pk>/delete", DeletePollQuestion.as_view(), name="poll.question.delete"),
    # PollAnswer
    path("<int:poll_id>/question/<int:question_id>/answer/create", CreatePollAnswer.as_view(),
        name="poll.answer.create"
    ),
    path("<int:poll_id>/question/<int:question_id>/answer/<int:pk>/update", UpdatePollAnswer.as_view(),
        name="poll.answer.update"
    ),
    path("<int:poll_id>/question/<int:question_id>/answer/<int:pk>/delete", DeletePollAnswer.as_view(),
        name="poll.answer.delete"
    ),
]

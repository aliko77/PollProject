from django.db import models
from django.conf import settings
from django.utils.text import slugify
from .utils import PollQuestionChoices


# Create your models here.

class Poll(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(editable=False, null=True, blank=True, unique=True, db_index=True)
    meta_title = models.CharField(max_length=100, null=True, blank=True)
    tags = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    starts_at = models.DateTimeField(null=True, blank=True,
        help_text="date and time at which the poll open up for voting"
    )
    ends_at = models.DateTimeField(null=True, blank=True,
        help_text="date and time at which the poll closes for voting"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Anket"
        verbose_name_plural = "Anketler"

    def _get_unique_slug(self) -> str:
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Poll.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class PollQuestion(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    type = models.CharField(max_length=5, choices=PollQuestionChoices.get_choices(),
        default=PollQuestionChoices.get_default()
    )
    content = models.TextField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Anket Soruları"
        verbose_name_plural = "Anket Soruları"


class PollAnswer(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    question = models.ForeignKey(
        PollQuestion,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    meta = models.TextField(null=True, blank=True)
    content = models.TextField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]


class PollVote(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    question = models.ForeignKey(
        PollQuestion,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    answer = models.ForeignKey(
        PollAnswer,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]


class PollPrivateLink(models.Model):
    pool = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    link = models.TextField()
    amount = models.PositiveBigIntegerField()
    usage = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

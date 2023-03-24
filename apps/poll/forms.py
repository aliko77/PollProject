from django import forms


class CreatePollForm(forms.Form):
    title = forms.CharField(required=True)
    description = forms.CharField(widget=forms.Textarea, required=False)
    tags = forms.CharField(required=True, label="Etiketler")
    is_active = forms.BooleanField(required=True)
    is_private = forms.BooleanField(required=True)


class CreatePollQuestionForm(forms.Form):
    type = forms.CharField(required=True)
    content = forms.CharField(required=True)
    is_active = forms.BooleanField(required=True)


class CreatePollAnswerForm(forms.Form):
    content = forms.CharField(required=True)
    meta = forms.CharField(required=False)
    is_active = forms.BooleanField(required=True)

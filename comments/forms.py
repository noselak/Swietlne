from django import forms

from .models import Comment


class CommentCreateForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    comment_username = forms.CharField(
            label="Imię",
            widget=forms.TextInput(attrs={'class': 'form-control'}))
    comment_body = forms.CharField(
            label="Komentarz",
            widget=forms.Textarea(attrs={'class': 'form-control'}))

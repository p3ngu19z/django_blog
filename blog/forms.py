from django import forms


class CommentForm(forms.Form):
    username = forms.CharField(max_length=200)
    text = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()

from django import forms


class CommentForm(forms.Form):
    username = forms.CharField(max_length=200)
    text = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()


class BioForm(forms.Form):
    bio = forms.CharField(widget=forms.Textarea, max_length=600)


class AvatarForm(forms.Form):
    avatar = forms.ImageField()

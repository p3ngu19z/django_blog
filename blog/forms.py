from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)


class BioForm(forms.Form):
    bio = forms.CharField(widget=forms.Textarea, max_length=600)


class AvatarForm(forms.Form):
    avatar = forms.ImageField()


class PostForm(forms.Form):
    headline = forms.CharField(max_length=300)
    category = forms.CharField(max_length=50)
    content = forms.CharField(widget=CKEditorUploadingWidget())
    image = forms.ImageField()

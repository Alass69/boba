from django import forms
from .models import Comment
from django.contrib.auth.forms import UserCreationForm

class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Comment
        fields = ['content', 'parent_id']

    def clean_parent_id(self):
        parent_id = self.cleaned_data['parent_id']
        if parent_id:
            try:
                Comment.objects.get(pk=parent_id)
            except Comment.DoesNotExist:
                raise forms.ValidationError("Invalid parent comment ID.")
        return parent_id

class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

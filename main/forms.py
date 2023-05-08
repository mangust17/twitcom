from .models import Post
from django import forms
from .models import Profile
from django.forms import ModelForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'video']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название поста'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите содержимое поста'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def save(self, user):
        post = Post(title=self.cleaned_data['title'],
                    content=self.cleaned_data['content'],
                    image=self.cleaned_data.get('image'),
                    video=self.cleaned_data.get('video'),
                    user=user)
        post.save()
        return post


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profileimg']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Расскажите о себе'}),
            'profileimg': forms.FileInput(attrs={'class': 'form-control-file'})
        }

    def save(self, commit=True, user=None):
        profile = super().save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return profile

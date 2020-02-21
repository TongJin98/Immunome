from django import forms
from .models import Anchor

class UploadFileForm(forms.ModelForm):
    #description=forms.CharField()
    document = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Anchor
        fields = ('document',)
        #fields = ('description', 'document')

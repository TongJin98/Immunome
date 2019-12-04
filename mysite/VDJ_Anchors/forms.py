from django import forms
from .models import Anchor

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Anchor
        fields = ('description', 'document', )

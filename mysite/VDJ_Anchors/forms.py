from django import forms
from .models import Anchor

FORMAT_CHOICES = [
    ('excel', 'EXCEL'),
    ('csv', 'CSV'),
]

class UploadFileForm(forms.ModelForm):
    #description=forms.CharField()
    document = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    Output_Formats = forms.MultipleChoiceField(
            required=True,
            widget=forms.CheckboxSelectMultiple,
            choices=FORMAT_CHOICES,
    )

    class Meta:
        model = Anchor
        fields = ('document','Output_Formats')
        #fields = ('description', 'document')



class SelectForm(forms.Form):
    Output_Formats = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=FORMAT_CHOICES,
    )

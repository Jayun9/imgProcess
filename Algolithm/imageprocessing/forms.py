from django import forms
from .models import ImageUploadModel

class UploadImageForm(forms.Form):
    image = forms.ImageField()
    
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUploadModel
        fields = ('image',)

from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):

   class Meta:
      model = Document
      fields = ['docfile']




# Работает вариант 2
# class DocumentForm(forms.ModelForm):
#
#    class Meta:
#       model = Document
#       fields = ['docfile']
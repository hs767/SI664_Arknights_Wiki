
from django import forms
from django.core.exceptions import ValidationError
from django.core import validators

# strip means to remove whitespace from the beginning and the end before storing the column
class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)
    rating = forms.IntegerField(required=True, max_value=5, min_value=0)

#class RatingForm(forms.Form):
#    rating = forms.IntegerField(required=True, max_value=5, min_value=0)

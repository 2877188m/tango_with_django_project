from django import forms
from rango.models import Category, Page

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length = 128, help_text = "Please enter the category name.")
    views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    likes = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    slug = forms.CharField(widget = forms.HiddenInput(), required = False)

    #Inline class, provides additional data on the form
    #Associates the ModelForm to a model
    class Meta:
        model = Category
        fields = ("name",)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length = 128, help_text = "Please enter the title of the page.")
    url = forms.URLField(max_length = 200, help_text = "Please enter the URL of the page.")
    views = forms.ImageField(widget = forms.HiddenInput(), initial = 0)

    #Inline class, provides additional data on the form
    #Associates the ModelForm to a model, excludes the foreign key
    class Meta:
        model = Page
        exclude = ("category",)
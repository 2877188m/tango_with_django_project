from django import forms
from rango.models import Category, Page, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length = Category.NAME_MAX_LENGTH, help_text = "Please enter the category name.")
    views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    likes = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    slug = forms.CharField(widget = forms.HiddenInput(), required = False)

    #Inline class, provides additional data on the form
    #Associates the ModelForm to a model
    class Meta:
        model = Category
        fields = ("name",)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length = Page.TITLE_MAX_LENGTH, help_text = "Please enter the title of the page.")
    url = forms.URLField(max_length = 200, help_text = "Please enter the URL of the page.")
    views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)

    #Inline class, provides additional data on the form
    #Associates the ModelForm to a model, excludes the foreign key
    class Meta:
        model = Page
        exclude = ("category",)

    #Overriden clean() method to verify URL structure
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get("url")

        #If url exist, but doesnt start with http://
        if url and not url.startswith("https://"):
            url = f"http://{url}"
            cleaned_data["url"] = url
        
        return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())

    #Inline class for additional data, associating the form to the model
    class Meta:
        model = User
        fields = ("username", "email", "password",)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("website", "picture",)
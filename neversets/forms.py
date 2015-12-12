from django import forms
from .models import UserProfile

class SignupForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('email', 'first_name', 'last_name')
        field_order = ['email', 'password1', 'password2', 'first_name', 'last_name', 'want_email']

    def signup(self, request, user):
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

class RequestFriend(forms.Form):
    request_user = forms.EmailField(label='Enter email address', max_length = 100)

class Accept(forms.Form):
    accept_user = forms.CharField(max_length = 100, widget=forms.HiddenInput())

class Unfriend(forms.Form):
    unfriend_user = forms.CharField(max_length = 100, widget=forms.HiddenInput())

class Decline(forms.Form):
    decline_user = forms.CharField(max_length = 100, widget=forms.HiddenInput())
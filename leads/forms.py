# we use this app to create our own forms instead of using django default forms
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Agent, Lead, User #Agent

User = get_user_model()

class LeadModelForm(forms.ModelForm):
    class Meta: # where we specify inf about form
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            #'agent',
            'description',
            'phone_number',
            'email'
        )

class LeadModelOrganizerForm(forms.ModelForm):
    class Meta: # where we specify inf about form
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
            'description',
            'phone_number',
            'email'
        )
    def __init__(self, *args, **kwargs):
        
        self.request = kwargs.pop('request')
        super(LeadModelOrganizerForm, self).__init__(*args, **kwargs)

        self.fields['agent'].queryset = Agent.objects.filter(organization_id=self.request.user.userprofile)


class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
        field_classes = {'username': UsernameField}

class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta: # where we specify inf about form
        model = Lead
        fields = (
            'category',
        )















# class AssignAgentForm(forms.Form):
#     agent = forms.ModelChoiceField(queryset=Agent.objects.none())

#     #filter agents from our organization
#     def __init__(self, *args, **kwargs):
#         request = kwargs.pop("request")
#         agents = Agent.objects.filter(organization=request.user.userprofile)
#         super(AssignAgentForm, self).__init__(*args, **kwargs)
#         self.fields["agent"].queryset = agents
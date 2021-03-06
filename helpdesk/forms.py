from django import forms
from .models import *
from django.forms import ModelChoiceField

class NewComment(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    document = forms.FileField(required=False)
class NewTopicForPas(forms.Form):

    title = forms.CharField()

    priority = forms.ChoiceField(choices=PRIORITY_OPTIONS, required=True, label='Priority')

    content = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
        try:
            dynamic_choices = kwargs.pop('dynamic_choices')
        except KeyError:
            dynamic_choices = None # if normal form
        super(NewTopicForPas, self).__init__(*args, **kwargs)
        if dynamic_choices is not None:
            self.fields['department'] = ModelChoiceField(
                                          queryset=dynamic_choices)
    class Meta:
        model = Department

class NewTopicForPdi(forms.Form):

    def __init__(self, *args, **kwargs):
        try:
            dynamic_choices = kwargs.pop('dynamic_choices')
        except KeyError:
            dynamic_choices = None # if normal form
        super(NewTopicForPdi, self).__init__(*args, **kwargs)
        if dynamic_choices is not None:
            self.fields['subject'] = ModelChoiceField(
                                          queryset=dynamic_choices)

    title = forms.CharField()

    priority = forms.ChoiceField(choices=PRIORITY_OPTIONS, required=True, label='Priority')

    content = forms.CharField(widget=forms.Textarea, required=True)

    subject = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = Subject

class EmployeeChooser(forms.Form):

    employee = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        try:
            dynamic_choices = kwargs.pop('dynamic_choices')
        except KeyError:
            dynamic_choices = None # if normal form
        super(EmployeeChooser, self).__init__(*args, **kwargs)
        if dynamic_choices is not None:
            self.fields['employee'] = ModelChoiceField(
                                          queryset=dynamic_choices)
    class Meta:
        model = User

class TeacherChooser(forms.Form):

    teacher = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        try:
            dynamic_choices = kwargs.pop('dynamic_choices')
        except KeyError:
            dynamic_choices = None # if normal form
        super(TeacherChooser, self).__init__(*args, **kwargs)
        if dynamic_choices is not None:
            self.fields['teacher'] = ModelChoiceField(queryset=dynamic_choices)
    class Meta:
        model = User

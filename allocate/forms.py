from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from .models import Doer, Chore, Household, Weight
    
class AddChoreForm(forms.ModelForm):

    class Meta:
        model = Chore
        fields = ['name', 'isFixed', 'doer', 'fixedValue']

class AddDoerForm(forms.ModelForm):

    class Meta:
        model = Doer
        fields = ['name']
        
class AddWeightForm(forms.Form):

    value=forms.FloatField(widget = forms.NumberInput(attrs = {'onchange' : "updateTotal();", 'class': 'weightInput'}))
    
    def __init__(self,*args,**kwargs):
        self.chore = kwargs.pop('chore')
        self.doer = kwargs.pop('doer')
        super(AddWeightForm,self).__init__(*args,**kwargs)
        
class BaseWeightFormSet(forms.BaseFormSet):

    def __init__(self, *args, **kwargs):
        self.doer = kwargs.pop('doer')
        super(BaseWeightFormSet,self).__init__(*args,**kwargs)

    def get_form_kwargs(self, index):
        kwargs = super(BaseWeightFormSet, self).get_form_kwargs(index)
        kwargs['chore'] = kwargs['doer'].household.chore_set.all()[index]
        kwargs['doer']  = kwargs['doer']
        print('{}: {}'.format(kwargs['doer'].name, kwargs['chore'].name))
        return kwargs
        
    def get_total_weights(self):
        self.total = sum([sum([field.value() if not(field.value() == None) else 0 for field in form]) for form in self.forms])

    
            




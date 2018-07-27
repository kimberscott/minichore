from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from .models import Doer, Chore, Household, Weight
from decimal import Decimal

class HouseholdLookupForm(forms.Form):
    name = forms.CharField(help_text='Enter the name of the household you want to find. This is case-sensitive and should exactly match the name you used before.')
    
    def clean_name(self):
        data = self.cleaned_data['name']
        if not Household.objects.filter(name=data).exists():
            raise forms.ValidationError(_("Sorry, we can't find that household in the database."), code="invalid")
        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data
    
class HouseholdEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HouseholdEditForm, self).__init__(*args)
        self.household = kwargs['household']
        
    def clean(self):
        """Checks that household is in editing state."""
        cleaned_data = super().clean()
        if any(self.errors):
            # Don't bother validating unless each field is valid on its own
            return
        if not self.household.editing:
            raise forms.ValidationError("Household is not in editing mode.")
    
class AddChoreForm(HouseholdEditForm):

    class Meta:
        model = Chore
        fields = ['name', 'isFixed', 'doer', 'fixedValue']
        
    def __init__(self, *args, **kwargs):
        super(AddChoreForm, self).__init__(*args, **kwargs)
        chore = kwargs.get('chore', None)
        if chore is not None:
        	self.initial = {'name': chore.name, 'isFixed': chore.isFixed, 'doer': chore.doer.pk if chore.doer else '', 'fixedValue': chore.fixedValue}
        doers = self.household.doer_set.all()
        doer_field = self.fields['doer'].widget
        doer_choices = []
        doer_choices.append(('', '---------'))
        for doer in doers:
            doer_choices.append((doer.pk, doer.name))
        doer_field.choices = doer_choices
        
    # TODO: validation if fixed!!
        

class AddDoerForm(HouseholdEditForm):

    class Meta:
        model = Doer
        fields = ['name']
        
    def __init__(self, *args, **kwargs):
        super(AddDoerForm, self).__init__(*args, **kwargs)
        doer = kwargs.get('doer', None)
        if doer is not None:
        	self.initial = {'name': doer.name}
        
class AddWeightForm(forms.Form):

    value=forms.DecimalField(widget = forms.NumberInput(attrs = {'step': 0.01, 'onchange' : "updateTotal();", 'class': 'freeWeightInput'}))
    
    def __init__(self,*args,**kwargs):
        self.chore = kwargs.pop('chore')
        self.doer = kwargs.pop('doer')
        super(AddWeightForm,self).__init__(*args,**kwargs)
        if self.chore.isFixed:
            self.fields['value'].widget.attrs['readonly'] = True
            self.fields['value'].initial = self.chore.fixedValue
            self.fields['value'].required = False
        
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
        return sum([form.chore.fixedValue if form.chore.isFixed 
            else Decimal(form['value'].value()) if not(form['value'].value() == None) else 0 for form in self.forms])

    def clean(self):
        """Checks that total of all weights is 100. Weights may be negative."""
        if any(self.errors):
            # Don't bother validating unless each form is valid on its own
            return
        if self.get_total_weights() != 100:
            raise forms.ValidationError("Weights must sum to 100; try normalizing.")


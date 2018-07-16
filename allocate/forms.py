from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from .models import Doer, Chore, Household
    
class AddChoreForm(ModelForm):

	class Meta:
		model = Chore
		fields = ['name', 'isFixed', 'doer', 'fixedValue']
    
#    def clean_renewal_date(self):
#         data = self.cleaned_data['renewal_date']
#         
#         #Check date is not in past. 
#         if data < datetime.date.today():
#             raise ValidationError(_('Invalid date - renewal in past'))
# 
#         #Check date is in range librarian allowed to change (+4 weeks).
#         if data > datetime.date.today() + datetime.timedelta(weeks=4):
#             raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
# 
#         # Remember to always return the cleaned data.
#         return data

class AddDoerForm(ModelForm):

	class Meta:
		model = Doer
		fields = ['name']
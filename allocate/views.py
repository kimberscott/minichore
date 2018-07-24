from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.forms import formset_factory

from .models import Household, Doer, Chore, Allocation, Weight
from .forms import AddChoreForm, AddDoerForm, AddWeightForm, BaseWeightFormSet

# Create your views here.
class HouseholdDetailView(generic.DetailView):
    model = Household
    
class HouseholdCreate(CreateView):
    model = Household
    fields = ['name']
    
def create_doer(request, pk):
    household = get_object_or_404(Household, id=pk)
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = AddDoerForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            doer = Doer(household=household,
                name=form.cleaned_data['name']
            )
            doer.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('household-detail', args=[pk]))

    # If this is a GET (or any other method) create the default form.
    else:
        form = AddDoerForm()

    return render(request, 'allocate/doer_form.html', {'form': form, 'household':household})
    
def enter_weights(request, pk):
	doer = get_object_or_404(Doer, id=pk)
	household = doer.household
	chores = household.chore_set.all()
	nChores = len(chores)
	AddWeightFormFormSet = formset_factory(AddWeightForm, formset=BaseWeightFormSet)
	
	if request.method == 'POST':
		formset = AddWeightFormFormSet(request.POST, form_kwargs={'doer': doer}, doer=doer)
		if formset.is_valid(): # Save all the weights
			for f in formset.forms:
				ch = f.chore
				v = f.cleaned_data['value']
				try: # if weight already exists, update value
					w = doer.weight_set.get(chore=ch)
					w.value = v
					w.save()
				except: # otherwise create weight
					w = Weight(value=v, doer=doer, chore=ch)
					w.save()
			return HttpResponseRedirect(reverse('household-detail', args=[household.id]))
	else:
		nChores = len(household.chore_set.all())
		data = {
			'form-TOTAL_FORMS': str(nChores),
			'form-INITIAL_FORMS': str(nChores),
			'form-MAX_NUM_FORMS': str(nChores),
		}
		initial = [{}] * nChores
		formset = AddWeightFormFormSet(data, doer=doer, initial=initial, form_kwargs={'doer': doer})

	return render(request, 'allocate/weights_form.html', {'formset': formset, 'doer':doer})
    
def create_chore(request, pk):
    household = get_object_or_404(Household, id=pk)
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = AddChoreForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
           
            chore = Chore(household=household,
                name=form.cleaned_data['name'],
                isFixed=form.cleaned_data['isFixed'],
                doer=form.cleaned_data['doer'],
                fixedValue=form.cleaned_data['fixedValue']
            )
            chore.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('household-detail', args=[pk]))

    # If this is a GET (or any other method) create the default form.
    else:
        form = AddChoreForm()

    return render(request, 'allocate/chore_form.html', {'form': form, 'household':household})
    
class ChoreDelete(DeleteView):
    model = Chore
    
    def get_success_url(self):
        return reverse_lazy('household-detail', args=[self.object.household.id])
        
class DoerDelete(DeleteView):
    model = Doer
    
    def get_success_url(self):
        return reverse_lazy('household-detail', args=[self.object.household.id])
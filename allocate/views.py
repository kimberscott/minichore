from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from .models import Household, Doer, Chore, Allocation, Weight
from .forms import AddChoreForm, AddDoerForm

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
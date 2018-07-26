from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.forms import formset_factory
from django.core.exceptions import ValidationError, PermissionDenied

import itertools

from .models import Household, Doer, Chore, Allocation, Weight
from .forms import AddChoreForm, AddDoerForm, AddWeightForm, BaseWeightFormSet, HouseholdLookupForm, HouseholdEditForm

# Model object creation/deletion/update views    
    
class HouseholdCreate(CreateView):
    model = Household
    fields = ['name']
    
def create_doer(request, pk):
    household = get_object_or_404(Household, id=pk)
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = AddDoerForm(request.POST, household=household)
        if form.is_valid():
            doer = Doer(household=household,
                name=form.cleaned_data['name']
            )
            doer.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('household-detail', args=[pk]))

    # If this is a GET (or any other method) create the default form.
    else:
        form = AddDoerForm(household=household)

    return render(request, 'allocate/doer_form.html', {'form': form, 'household':household})
    
def update_doer(request, pk):
    doer = get_object_or_404(Doer, pk=pk)
    household = doer.household
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = AddDoerForm(request.POST, household=household, doer=doer)
        if form.is_valid():
            doer.name = form.cleaned_data['name']
            doer.save()
            return HttpResponseRedirect(reverse('household-detail', args=[household.id]))

    # If this is a GET (or any other method) create the default form.
    else:
        form = AddDoerForm(household=household, doer=doer)

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
                # Get appropriate value, either entered or fixed
                v = ch.fixedValue if ch.isFixed else f.cleaned_data['value']
                try: # if weight already exists, update value
                    w = doer.weight_set.get(chore=ch)
                    w.value = v
                    w.save()
                except: # otherwise create weight
                    w = Weight(value=v, doer=doer, chore=ch)
                    w.save()
            # Save the fact that this doer has entered weights
            doer.hasWeights = True
            doer.save()
            # Get rid of any previous allocations since scores will be incorrect
            household.allocation_set.all().delete()
            return HttpResponseRedirect(reverse('weights-overview', args=[household.id]))
    else:
        nChores = len(household.chore_set.all())
        data = {
            'form-TOTAL_FORMS': str(nChores),
            'form-INITIAL_FORMS': str(nChores),
            'form-MAX_NUM_FORMS': str(nChores),
        }
        initial = [{}] * nChores
        formset = AddWeightFormFormSet(data, doer=doer, initial=initial, form_kwargs={'doer': doer})

    return render(request, 'allocate/weights_form.html', {'formset': formset, 'doer':doer, 'household': household})
    
def create_chore(request, pk):
    household = get_object_or_404(Household, id=pk)
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = AddChoreForm(request.POST, household=household)
        if form.is_valid():
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
        form = AddChoreForm(household=household)

    return render(request, 'allocate/chore_form.html', {'form': form, 'household':household})
    
def update_chore(request, pk):
    chore = get_object_or_404(Chore, pk=pk)
    household = chore.household
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = AddChoreForm(request.POST, household=household)
        if form.is_valid():
            chore.name = form.cleaned_data['name']
            chore.isFixed = form.cleaned_data['isFixed']
            chore.doer = form.cleaned_data['doer']
            chore.fixedValue = form.cleaned_data['fixedValue']
            chore.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('household-detail', args=[household.id]))
    # If this is a GET (or any other method) create the default form.
    else:
        form = AddChoreForm(household=household, chore=chore)

    return render(request, 'allocate/chore_form.html', {'form': form, 'household':household})
    
class ChoreDelete(DeleteView):
    model = Chore
    
    def get_success_url(self):
        return reverse_lazy('household-detail', args=[self.object.household.id])
        
    def get_object(self):
        """ Make sure household is in editing mode, or raise 403 """
        chore = super(ChoreDelete, self).get_object()
        if not chore.household.editing:
            raise PermissionDenied("Household is not in editing mode.")
        return chore
        
class DoerDelete(DeleteView):
    model = Doer
    
    def get_success_url(self):
        return reverse_lazy('household-detail', args=[self.object.household.id])
        
    def get_object(self):
        """ Make sure household is in editing mode, or raise 403 """
        chore = super(DoerDelete, self).get_object()
        if not chore.household.editing:
            raise PermissionDenied("Household is not in editing mode.")
        return chore
        
# Display information views        

class HouseholdDetailView(generic.DetailView):
    model = Household
    
    def dispatch(self, request, *args, **kwargs):
        household = self.get_object()
        request.session['household'] = household
        if 'changeLock' in kwargs:
            if kwargs['changeLock'] == 'unlock':
                household.allocation_set.all().delete()
                Weight.objects.filter(doer__household=household).delete()
                # Set all doers as not having weights set
                for doer in household.doer_set.all():
                    doer.hasWeights = False
                    doer.save()
                household.editing = True
                household.save()
            elif kwargs['changeLock'] == 'lock':
                household.editing = False
                household.save()
        return super(HouseholdDetailView, self).dispatch(request, *args, **kwargs)
        
class HouseholdWeightsView(generic.DetailView):
    model = Household
    template_name = 'allocate/household_weights_overview.html'
    
class HouseholdLookup(FormView):
    template_name = 'allocate/household_form.html'
    form_class = HouseholdLookupForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        self.household = get_object_or_404(Household, name=form.cleaned_data['name'])
        return HttpResponseRedirect(reverse('household-detail', args=[self.household.id]))    
    
def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_households=Household.objects.all().count()
   
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_households':num_households, 'num_visits':num_visits},
    )
        
def generate_allocations(household):

    # Get rid of all other allocations for this household
    household.allocation_set.all().delete()
    # Get chore list
    chores = household.chore_set.all()
    # Get free chore list
    freeChores = household.chore_set.filter(isFixed=False)
    # Get fixed chore list
    fixedChores = household.chore_set.filter(isFixed=True)
    # Get doer list
    doers = household.doer_set.all()
    
    # For every possible mapping of doers to free chores...
    for doerAssignment in itertools.product(doers, repeat=len(freeChores)):
        # Create the allocation - 
        allo = Allocation(household=household)
        allo.save() # Must be saved before adding assignments
        # First assign fixed chores to their doers
        for ch in fixedChores:
            w = ch.doer.weight_set.get(chore=ch)
            allo.assignments.add(w)
        for (d, ch) in zip(doerAssignment, freeChores):
            w = d.weight_set.get(chore=ch)
            allo.assignments.add(w)
        allo.score = allo.calculateScore()
        print(allo.score)
        allo.save()
    
def allocation_detail(request, pkh, pka):
    household = get_object_or_404(Household, id=pkh)
    allocation = get_object_or_404(Allocation, id=pka)
    return render(request, 'allocate/allocation_detail.html', {'household':household, 'allocation': allocation})
    
class AllocationListView(generic.list.ListView):
    model = Allocation
    paginate_by = 25
    
    def get_queryset(self):
        household = get_object_or_404(Household, id=self.kwargs['pk'])
        if not household.allocation_set.all().exists():
            generate_allocations(household)
        return household.allocation_set.all()


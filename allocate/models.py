from django.db import models
import uuid
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Household(models.Model):
    """
    A class representing a household with chores to divy up.
    """

    # Members of household and chores within household are defined via Doer, Chore.

    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this household")
    allocations_are_current = models.BooleanField(default=False)
    name = models.CharField(max_length=40, help_text="Enter a name for the household (e.g., 'The Scotts')")

    # Methods
    def get_absolute_url(self):
         """
         Returns the url to access a particular Household
         """
         return reverse('household-detail', args=[str(self.id)])
    
    def __str__(self):
        """
        String for representing the Household object (in Admin site etc.)
        """
        return '{} ({})'.format(self.name, self.id)
        
    @property
    def have_all_weights(self):
        for doer in Doer.objects.filter(household=self):
            if not(doer.hasWeights):
                return False
        return True
        
class Doer(models.Model):
    """
    A class representing a person to assign chores to.
    """
    
    name = models.CharField(max_length=40, help_text="Enter the name of a household member")
    household = models.ForeignKey('Household', on_delete='CASCADE')
    hasWeights = models.BooleanField(default=False)

    # Metadata
    class Meta: 
        ordering = ["name"]
    
    def __str__(self):
        """
        String for representing the Doer object (in Admin site etc.)
        """
        return '{} (Household: {})'.format(self.name, self.household.name)
        
class Chore(models.Model):
    """
    A class representing a chore that needs to be assigned to someone.
    """

    # Fields
    name = models.CharField(max_length=40, help_text="Enter the name of a chore")
    household = models.ForeignKey('Household', on_delete='CASCADE')
    
    isFixed = models.BooleanField(default=False) 
    doer = models.ForeignKey('Doer', on_delete=models.SET_NULL, blank=True, null=True)
    fixedValue = models.FloatField(blank=True, null=True)

    # Metadata
    class Meta: 
        ordering = ["household", "name"]
    
    def __str__(self):
        """
        String for representing the Chore object (in Admin site etc.)
        """
        return '{} (Household: {})'.format(self.name, self.household.name)
        
class Weight(models.Model):
    """
    A class representing the cost one doer associates with a chore.
    """

    # Fields
    value = models.FloatField()
    chore = models.ForeignKey('Chore', on_delete='CASCADE')
    doer = models.ForeignKey('Doer', on_delete='CASCADE')

    # Metadata
    class Meta: 
        ordering = ["doer", "chore"]
    
    def __str__(self):
        """
        String for representing the Chore object (in Admin site etc.)
        """
        return '{}: {}, {}'.format(doer.name, chore.name, value)
        
class Allocation(models.Model):
    """
    A class representing an allocation of all chores in a household to doers.
    """

    # Fields
    household = models.ForeignKey('Household', on_delete='CASCADE')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this allocation")
    assignments = models.ManyToManyField(Weight, help_text='Weights for all doers for the chores they are assigned')

    def __str__(self):
        """
        String for representing the Chore object (in Admin site etc.)
        """
        return '{} (Household: {})'.format(self.name, self.household.name)
        
    @property
    def score(self):
        scores = []
        for d in Doer.objects.filter(household=self.household):
            dsAssignments = self.assignments.filter(doer=d)
            scores.append(sum([a.chore.value if a.chore.isFixed else a.value for a in dsAssignments]))
        return max(scores)
        
    # Metadata
    class Meta: 
        ordering = ["household"]
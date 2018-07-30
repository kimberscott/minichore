from django.db import models
import uuid
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from jsonfield import JSONField

class Household(models.Model):
    """
    A class representing a household with chores to divy up.
    """

    # Members of household and chores within household are defined via Doer, Chore.

    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this household")
    editing = models.BooleanField(default=True)
    name = models.CharField(max_length=40, unique=True, help_text="Enter a name for the household (e.g., 'The Scotts')")
    haveAllocations = models.IntegerField(default=0)

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
    household = models.ForeignKey('Household', on_delete=models.CASCADE)
    hasWeights = models.BooleanField(default=False)

    # Metadata
    class Meta: 
        ordering = ["name"]
    
    def __str__(self):
        """
        String for representing the Doer object (in Admin site etc.)
        """
        return '{} (Household: {})'.format(self.name, self.household.name)
        
    # Don't allow deletion when household is not in edit mode
    def delete(self, *args, **kwargs):
        if not self.household.editing:
            raise Exception('Household is not in editing mode.')
        super().delete(*args, **kwargs)
        
    # Do allow saving - name changes are ok and whether doer has weights will change!
        
class Chore(models.Model):
    """
    A class representing a chore that needs to be assigned to someone.
    """

    # Fields
    name = models.CharField(verbose_name='Chore name', max_length=40, help_text="Enter the name of a chore")
    household = models.ForeignKey('Household', on_delete=models.CASCADE)
    
    isFixed = models.BooleanField(verbose_name='Assigned?', default=False, help_text="Does this chore have to be done by a particular person?") 
    doer = models.ForeignKey('Doer', verbose_name='Assigned to', on_delete=models.SET_NULL, blank=True, null=True, help_text="If assigned, who has to do this chore?")
    fixedValue = models.DecimalField(verbose_name='Assigned value', max_digits=8, decimal_places=2, blank=True, null=True, help_text="If assigned, mutually chosen value of chore (out of 100)")

    # Metadata
    class Meta: 
        ordering = ["household", "name"]
    
    def __str__(self):
        """
        String for representing the Chore object (in Admin site etc.)
        """
        return '{} (Household: {}, isFixed: {}, fixedValue: {})'.format(self.name, self.household.name, self.isFixed, self.fixedValue)
  
  	# Don't allow deletion OR saving any changes unless household is in edit mode!
    def delete(self, *args, **kwargs):
        if not self.household.editing:
            raise Exception('Household is not in editing mode.')
        super().delete(*args, **kwargs)  
        
    def save(self, *args, **kwargs):
        if not self.household.editing:
            raise Exception('Household is not in editing mode.')
        super().save(*args, **kwargs)  
  
class Weight(models.Model):
    """
    A class representing the cost one doer associates with a chore.
    """

    # Fields
    value = models.DecimalField(max_digits=8, decimal_places=2)
    chore = models.ForeignKey('Chore', on_delete=models.CASCADE)
    doer = models.ForeignKey('Doer', on_delete='CASCADE')

    # Metadata
    class Meta: 
        ordering = ["chore", "doer"]
    
    def __str__(self):
        """
        String for representing the Chore object (in Admin site etc.)
        """
        return '{}: {}, {}'.format(self.doer.name, self.chore.name, self.value)
        
class Allocation(models.Model):
    """
    A class representing an allocation of all chores in a household to doers.
    """

    # Fields
    household = models.ForeignKey('Household', on_delete='CASCADE')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this allocation")
    assignments = models.ManyToManyField(Weight, help_text='Weights for all doers for the chores they are assigned')
    score = models.FloatField(default=100)
    allScores = JSONField(default={})
    
    class Meta: 
        ordering = ["id", "score"]

    def __str__(self):
        """
        String for representing the Allocation object (in Admin site etc.)
        """
        return '{} (Household: {})'.format(self.id, self.household.name)
        
    def calculateScore(self):
        scores = {}
        for d in self.household.doer_set.all():
            dsAssignments = self.assignments.filter(doer=d)
            scores[d.pk] = sum([a.chore.fixedValue if a.chore.isFixed else a.value for a in dsAssignments])
        return (max(scores.values()), scores)
        
    def position(self):
        return (Allocation.objects
        	.filter(household=self.household, score__lte=self.score)
            .exclude(id=self.id)
            .exclude(score=self.score, id__gte=self.id)
            .order_by('-score', 'id')
            .count()) + 1
        
    def next(self):
        return (Allocation.objects
            .filter(household=self.household, score__gte=self.score)
            .exclude(id=self.id)
            .exclude(score=self.score, id__lte=self.id)
            .order_by('score')
            .first())
    
    def prev(self):
        return (Allocation.objects
        	.filter(household=self.household, score__lte=self.score)
            .exclude(id=self.id)
            .exclude(score=self.score, id__gte=self.id)
            .order_by('-score')
            .first())
        
    # Metadata
    class Meta: 
        ordering = ["household", "score"]
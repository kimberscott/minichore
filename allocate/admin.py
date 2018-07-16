from django.contrib import admin
from .models import Household, Doer, Chore, Allocation, Weight

admin.site.register(Household)
admin.site.register(Doer)
admin.site.register(Chore)
admin.site.register(Allocation)
admin.site.register(Weight)
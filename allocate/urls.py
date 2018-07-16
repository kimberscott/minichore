from django.urls import path
from . import views

urlpatterns = [
	path('households/<uuid:pk>', views.HouseholdDetailView.as_view(), name='household-detail'),
	path('households/create/', views.HouseholdCreate.as_view(), name='household-create'),
	path('households/<uuid:pk>/createChore/', views.create_chore, name='chore-create'),
	path('households/<uuid:pk>/createDoer/', views.create_doer, name='doer-create'),
]
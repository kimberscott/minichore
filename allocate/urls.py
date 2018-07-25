from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('households/<uuid:pk>', views.HouseholdDetailView.as_view(), name='household-detail'),
	path('households/create/', views.HouseholdCreate.as_view(), name='household-create'),
	path('households/lookup/', views.HouseholdLookup.as_view(), name='household-lookup'),
	path('households/<uuid:pk>/createChore/', views.create_chore, name='chore-create'),
	path('households/<uuid:pk>/createDoer/', views.create_doer, name='doer-create'),
	path('households/<uuid:pk>/weights/', views.HouseholdWeightsView.as_view(), name='weights-overview'),
	path('households/doers/<int:pk>/enterWeights/', views.enter_weights, name='enter-weights'),
	path('households/doers/<int:pk>/delete/', views.DoerDelete.as_view(), name='doer-delete'),
	#path('households/<uuid:pk>/generateAllocations/', views.generate_allocations, name='generate-allocations'),
	path('households/<uuid:pkh>/allocations/<uuid:pka>/', views.allocation_detail, name='allocation-detail'),
	path('households/<uuid:pk>/allocations/', views.AllocationListView.as_view(), name='allocation-list'),
	path('households/chores/<int:pk>/delete/', views.ChoreDelete.as_view(), name='chore-delete'),
]
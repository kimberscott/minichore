from django.urls import path
from . import views

urlpatterns = [
	path('households/<uuid:pk>', views.HouseholdDetailView.as_view(), name='household-detail'),
	path('households/create/', views.HouseholdCreate.as_view(), name='household-create'),
	path('households/<uuid:pk>/createChore/', views.create_chore, name='chore-create'),
	path('households/<uuid:pk>/createDoer/', views.create_doer, name='doer-create'),
	path('households/doers/<int:pk>/enterWeights/', views.enter_weights, name='enter-weights'),
	path('households/chores/<int:pk>/delete/', views.ChoreDelete.as_view(), name='chore-delete'),
	path('households/doers/<int:pk>/delete/', views.DoerDelete.as_view(), name='doer-delete'),
]
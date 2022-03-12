from django.urls import path
from .views import (
    LeadDeleteView, landing_page, lead_list, lead_detail, lead_create, lead_update, lead_delete,
    LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView
)

app_name = "leads"

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'), # leads/all/, views.py function/class, variable = path
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),
]



# ============= ERRORS ==============
# If we put /create path before <pk>
# Django will understand that /create path
# It's a primary key so it will get an error

# TO AVOID THIS ERROR

# we change path('<pk>')
# to path ('<int:pk>')
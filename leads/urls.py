from django.urls import path
from .views import ( 
    LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView,
    CategoryListView
)

app_name = "leads"

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'), # leads/all/, views.py function/class, variable = path
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),
    path('categories/', CategoryListView.as_view(), name='category-list')
]



# ============= ERRORS ==============
# If we put /create path before <pk>
# Django will understand that /create path
# It's a primary key so it will get an error

# TO AVOID THIS ERROR

# we change path('<pk>')
# to path ('<int:pk>')
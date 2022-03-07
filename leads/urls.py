from django.urls import path
from .views import lead_list, lead_detail, lead_create, lead_update, lead_delete

app_name = "leads"

urlpatterns = [
    path('', lead_list, name='lead-list'), # leads/all/, views.py function
    path('<int:pk>/', lead_detail, name='lead-detail'),
    path('<int:pk>/update/', lead_update, name='lead-update'),
    path('<int:pk>/delete/', lead_delete, name='lead-delete'),
    path('create/', lead_create, name='lead-create'),
]



# ============= ERRORS ==============
# If we put /create path before <pk>
# Django will understand that /create path
# It's a primary key so it will get an error

# TO AVOID THIS ERROR

# we change path('<pk>')
# to path ('<int:pk>')
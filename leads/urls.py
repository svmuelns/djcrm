from django.urls import path
from .views import lead_list, lead_detail, lead_create

app_name = "leads"

urlpatterns = [
    path('', lead_list), # leads/all/, views.py function
    path('<int:pk>/', lead_detail),
    path('create/', lead_create)
]



# ============= ERRORS ==============
# If we put /create path before <pk>
# Django will understand that /create path
# It's a primary key so it will get an error

# TO AVOID THIS ERROR

# we change path('<pk>')
# to path ('<int:pk>')
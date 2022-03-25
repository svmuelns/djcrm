from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, 
    PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import path, include
from leads.views import LandingPageView, SignupView #landing_page

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', landing_page, name='landing-page'),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('leads/', include('leads.urls', namespace="leads")), # leads/urls.py will take care of the urls in it
    path('agents/', include('agents.urls', namespace="agents")),
    path('signup/', SignupView.as_view(), name="signup"),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('login/', LoginView.as_view(), name='login'), # you can enter with your django superuser
    path('logout/', LogoutView.as_view(), name='logout')
]
if settings.DEBUG: # if we are in debug mode, add this url pattern
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
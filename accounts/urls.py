from django.urls import path
from virtual_app .endpoints.signup import signup

app_name = 'accounts'

urlpatterns = [
    # Other URL patterns here...
    path('signup/', signup, name='signup'),
]

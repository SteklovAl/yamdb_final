from api.views import signup_post, token_post
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('signup/', signup_post),
    path('token/', token_post),
]

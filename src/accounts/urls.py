from django.urls import path
from accounts.views import login_view, logout_view, register_view, update_view


urlpatterns = [

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('update/', update_view, name='update'),
]
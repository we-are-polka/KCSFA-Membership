from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile_page, name='profile'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_info/', views.update_info, name='update_info'),
    path('events/', views.all_events, name='events'),
    path('single_event/<int:event_id>', views.single_event, name='single_event'),

]
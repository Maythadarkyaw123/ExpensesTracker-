from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
#from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('landing/', views.landing_view, name='landing'),
    #path('add-transaction/', views.add_transaction, name='add_transaction'),  
    #path('view-transactions/', views.view_transactions, name='view_transactions'),  
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/complete/', views.password_reset_complete, name='password_reset_complete'),
    #path('admin/', admin.site.urls),
    #path('', include('tracker.urls')),

]

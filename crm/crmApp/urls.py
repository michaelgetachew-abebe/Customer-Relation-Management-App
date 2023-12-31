from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/', views.register_user, name='register_user'),
    path('record/<int:id>', views.customer_record, name='record'),
    path('delete_record/<int:id>', views.delete, name='delete_record'),
    path('add_record', views.add_record, name='add_record'),
    path('edit_record/<int:id>', views.edit_record, name='edit_record'),
]
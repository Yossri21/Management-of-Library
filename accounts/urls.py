from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('member_add', views.member_add, name='member_add'),
    path('member_list', views.member_list, name='member_list'),
    path('members/<int:id>', views.member_detail, name='member_detail'),
    path('members/delete/<int:id>', views.member_delete, name='member_delete'),
    path('member_search', views.member_search, name='member_search'),
    path('librarian_liste', views.librarian_liste, name='librarian_liste'),
    path('librarian/delete/<int:id>', views.librarian_delete, name='librarian_delete'),
    path('librarian/<int:id>', views.librarian_update, name='librarian_update'),

]

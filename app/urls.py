from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('products/', views.products, name='products'),
    path('user/', views.userPage, name="user-page"),
    path('account/', views.accountSettings, name="account"),

    # search path
    path('search/', views.search_view, name='search'),
    # path('products_search/', views.products_search, name='products_search'),
    

    path('create_order/<str:pk>/', views.create_order, name='create_order'),
    path('update_order/<str:pk>/', views.update_order, name='update_order'),
    path('delete_order/<str:pk>/', views.delete_order, name='delete_order'),


    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
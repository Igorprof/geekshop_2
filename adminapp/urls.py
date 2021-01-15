from django.urls import path

import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name='index'), 
    path('users/', adminapp.UserListView.as_view(), name='admin_users'),
    path('users/create/', adminapp.UserCreateView.as_view(), name='admin_users_create'),
    path('users/update/<int:pk>/', adminapp.UserUpdateView.as_view(), name='admin_users_update'),
    path('users/remove/<int:pk>/', adminapp.UserDeleteView.as_view(), name='admin_users_remove'),
    path('product_categories/', adminapp.ProductCategoriesListView.as_view(), name='admin_product_categories'),
    path('product_categories/update/<int:pk>/', adminapp.ProductCategoriesUpdateView.as_view(), name='admin_product_categories_update'),
    path('product_categories/create/', adminapp.ProductCategoryCreateView.as_view(), name='admin_product_categories_create'),
    path('product_categories/remove/<int:pk>/', adminapp.ProductCategoryDeleteView.as_view(), name='admin_product_categories_remove'),
]
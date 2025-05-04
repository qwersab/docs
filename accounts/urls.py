from django.urls import path
from .views import (
    RegisterView, LoginView, UserInfoView, UpdateUserView, 
    UploadProfilePictureView, ChangePasswordView,
    CreateProductView, ListUserProductsView, ProductCategoriesView,
    UploadProductImageView, ListAllProductsView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserInfoView.as_view(), name='user-info'),
    path('user/update/', UpdateUserView.as_view(), name='user-update'),
    path('user/upload-avatar/', UploadProfilePictureView.as_view(), name='upload-avatar'),
    path('user/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('products/create/', CreateProductView.as_view(), name='create-product'),
    path('user/products/', ListUserProductsView.as_view(), name='user-products'),
    path('products/categories/', ProductCategoriesView.as_view(), name='product-categories'),
    path('products/upload-image/', UploadProductImageView.as_view(), name='upload-product-image'),
    path('products/', ListAllProductsView.as_view(), name='list-all-products'),
]
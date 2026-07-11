from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/products/', views.ProductListCreateAPIView.as_view()),
    path('api/v1/products/<int:id>/', views.ProductDetailAPIView.as_view()),
    path('api/v1/categories/', views.CategoryListCreateAPIView.as_view()),
    path('api/v1/categories/<int:id>/', views.CategoryDetailAPIView.as_view()),
    path('api/v1/reviews/', views.ReviewListCreateAPIView.as_view()),
    path('api/v1/reviews/<int:id>/', views.ReviewDetailAPIView.as_view()),
    path('api/v1/products/reviews/', views.ProductsReviewsAPIView.as_view()),
]
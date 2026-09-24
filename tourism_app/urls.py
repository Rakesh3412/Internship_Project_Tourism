from django.urls import path
from . import views

app_name = 'tourism_app'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('states/', views.states_list_view, name='states_list'),
    path('states/<slug:slug>/', views.state_detail_view, name='state_detail'),
    path('places/', views.places_list_view, name='places_list'),
    path('places/<slug:slug>/', views.place_detail_view, name='place_detail'),
    path('categories/<slug:slug>/', views.category_detail_view, name='category_detail'),
    path('places/<int:place_id>/review/', views.submit_review_view, name='submit_review'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:place_id>/', views.toggle_wishlist_view, name='toggle_wishlist'),
    path('inquiry/', views.submit_inquiry_view, name='submit_inquiry'),
    path('api/search/', views.api_search_view, name='api_search'),
]

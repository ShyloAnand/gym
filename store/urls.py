from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name="login"),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('sports/', views.sports, name='sports'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('diet-plan/', views.diet_plan, name='diet_plan'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('fitness/', views.fitness, name='fitness'),
    path('payment/', views.payment, name='payment'),

]
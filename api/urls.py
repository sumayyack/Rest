from django.urls import path
from api import views
urlpatterns=[
    path('products/',views.MyProducts.as_view()),
    path('products/accounts/register',views.RegistrationView.as_view()),
    path('products/accounts/signin',views.Login.as_view()),
    path('products/accounts/signout',views.Logout.as_view()),
    path('purchases/',views.Purchases.as_view())
]
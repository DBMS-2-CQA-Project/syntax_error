from django.urls import path
from . import views

urlpatterns=[
  path('',views.home,name="djsfhdj"),
  path('signin',views.signup,name="djsfhdj")
]
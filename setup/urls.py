from django.urls import path
from . import views

urlpatterns=[
  path('',views.signup,name="signup"),
  path('test',views.test,name="test"),
  # path('signin',views.signin,name="djsfhdj"),
  # path('signup',views.signup,name="djsfhdj"),
  # path('signindata',views.signinData,name="djsfhdj"),
  # path('signupdata',views.signupdata,name="djsfhdj")
]
from django.urls import path
from . import views

urlpatterns=[
  path('test',views.test,name="test"),
  path('editProfile',views.editProfile,name="editProfile"),
  # path('signin',views.signin,name="djsfhdj"),
  # path('signup',views.signup,name="djsfhdj"),
  # path('signindata',views.signinData,name="djsfhdj"),
  # path('signupdata',views.signupdata,name="djsfhdj")
  path('',views.home,name="djsfhdj"),
  path('signin',views.signin,name="djsfhdj"),
  path('signup',views.signup,name="djsfhdj"),
  path('edited',views.edited,name="djsfhdj"),
  path('search',views.search,name="djsfhdj"),
  path('eachpost',views.eachpost,name="djsfhdj"),

]
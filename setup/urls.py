from django.urls import path
from . import views
from django.contrib import admin  

urlpatterns=[
  path('signup',views.signup,name="signup"),
  path('editProfile',views.editProfile,name="editProfile"),
  path('',views.home,name="djsfhdj"),
  path('signin',views.signin,name="djsfhdj"),
  path('signup',views.signup,name="djsfhdj"),
  path('edited',views.profileEdited,name="djsfhdj"),
  path('createPost',views.createPost,name="djsfhdj"),
  path('PostCreated',views.PostCreated,name="CreatedPost"),

  path('AllYourPosts',views.AllYourPosts,name="AllYourPosts"),
  path('PostAnswer',views.PostAnswer,name="PostAnswer"),
  path('AnsweredPost',views.AnsweredPost,name="AnsweredPost"),
  path('search',views.search,name="djsfhdj"),
  path('eachpost',views.eachpost,name="djsfhdj"),
  path('logout',views.logout,name="logout"),

  path('Singlepost',views.Singlepost,name="Singlepost"),
  path('PostEdited',views.PostEdited,name="AllYourPosts"),
  path('EditedPostPage',views.PostEdited,name="EditedPostPage"),
  path('AddComment',views.AddComment,name="AddComment"),
  path('CommentAdded',views.CommentAdded,name="CommentAdded")
  # path('profile',views.profile,name="profile")
]
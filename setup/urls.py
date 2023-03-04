from django.urls import path
from . import views
from django.contrib import admin  

urlpatterns=[
  path('signup',views.signup,name="signup3"),
  path('editProfile',views.editProfile,name="editProfile"),
  path('',views.home,name="home"),
  path('signin',views.signin,name="sign-in"),
  # path('signup',views.signup,name="djsfhdj"),
  path('edited',views.profileEdited,name="djsfhdj"),
  path('createPost',views.createPost,name="djsfhdj"),
  path('PostCreated',views.PostCreated,name="CreatedPost"),

  path('AllYourPosts',views.AllYourPosts,name="AllYourPosts"),
  path('PostAnswer',views.PostAnswer,name="PostAnswer"),
  path('AnsweredPost',views.AnsweredPost,name="AnsweredPost"),
  path('search',views.search,name="djsfhdj"),
  path('eachpost',views.eachpost,name="djsfhdj"),
  path('VotesUpdate',views.Votes_Update,name= "Score"),
  path('logout',views.logout,name="logout"),

  path('Singlepost',views.Singlepost,name="Singlepost"),
  # path('PostEdited',views.PostEdited,name="AllYourPosts"),
  # path('EditedPostPage',views.PostEdited,name="EditedPostPage"),
  path('CommentAdded',views.CommentAdded,name="CommentAdded"),
  path('profile',views.profile,name='Profile'),
  path('editPost',views.editPost,name='editPost'),
  path('postEdited',views.postEdited,name='postEdited'),


 # path('OrderByUpvotes',views.OrderByUpvotes,name="OrderByUpvotes")
  # path('profile',views.profile,name="profile")

  
]
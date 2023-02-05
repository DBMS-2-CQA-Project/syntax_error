from django.shortcuts import render
from django.http import HttpResponse
from setup.models import users
from django.contrib import auth

# Create your views here.

def home(request):
  # queries=
  return render(request, 'index.html')

def signin(request):

  if request.method=='POST':
    id=request.POST.get('id')
    pw=request.POST.get('pw')
    print(id,pw)
    curr_user=users.objects.filter(id=id)
    print(curr_user)
    if not curr_user:
      print("dsskjds")
      return HttpResponse("Check your credential")
    else:
      return render(request, 'index.html',list(curr_user.values())[0])
  return render(request,'signin.html')

def signup(request):
  print(request.POST.get('email_mobno'))
  return render(request, 'signup.html')


# def signinData(request):
#   if request.method=='POST':


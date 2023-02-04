from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
  return render(request, 'index.html')

def signin(request):
  print(request.POST.get('email_mobno'))
  return render(request, 'signin.html')

def signup(request):
  print(request.POST.get('email_mobno'))
  return render(request, 'signup.html')


# def signinData(request):
#   if request.method=='POST':


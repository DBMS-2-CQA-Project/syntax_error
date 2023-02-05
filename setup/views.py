from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from setup.models import users
from django.contrib import auth

def test(request):
  
  # print(request.POST.get('email_mobno'))

  mydata = users.objects.all().values()

  # template = loader.get_template('template.html')
  context = {
    'mymembers': mydata
  }
  length=len(mydata)
  #print(mydata[length-1]['id'])
  new_id=1+mydata[length-1]['id']
  new_account_id=request.POST.get('account_id')
  new_reputation=0
  new_views=0
  new_down_votes=0
  new_up_votes=0
  new_display_name=request.POST.get('display_name')
  print(new_display_name)
  new_location=request.POST.get('location')
  new_about_me=request.POST.get('about_me')
  new_fellow=users(id=new_id,account_id=new_account_id,reputation=new_reputation,views=new_views,down_votes=new_down_votes,up_votes=new_up_votes,display_name=new_display_name,location=new_location,about_me=new_about_me)
  new_fellow.save()
  # new data
  mydata = users.objects.all().values()

  # template = loader.get_template('template.html')
  context = {
    'mymembers': mydata
  }
  # return HttpResponse(loader.get_template('test.html'),render(context, request))
  return render(request, 'test.html', context)

def home(request):
  # queries=
  return render(request, 'index.html')



def signin(request):

  if request.method=='POST':
    id=request.POST.get('id')
    pw=request.POST.get('display_name')
    print(id,pw)
    curr_user=users.objects.filter(id=id)
    print(curr_user)
    if not curr_user:
      return HttpResponse("Check your credential")
    else:
      return render(request, 'index.html',list(curr_user.values())[0])
  return render(request,'signin.html')

def signup(request):
  return render(request, 'signup.html')



# Check out template.html to see how the mymembers object
# was used in the HTML code. 
# Create your views here.

# def home(request):
#   return render(request, 'index.html')

# def signin(request):
#   print(request.POST.get('email_mobno'))
#   return render(request, 'signin.html')

# def signup(request):
#   print(request.POST.get('email_mobno'))
#   return render(request, 'signup.html')

  
# def signinData(request):
#   if request.method=='POST':


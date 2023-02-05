from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import users
from setup.models import users
from django.contrib import auth

dataIt=[0,0,0,0,0,0,0,0,0,0,0,0,0]

UserCurrent=users.objects.filter(id=2)
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

def edited(request):
  updated_account_id= request.POST['updated_account_id']
  updated_display_name = request.POST['updated_display_name']
  updated_location= request.POST['updated_location']
  updated_profile_image_url= request.POST['updated_profile_image_url']
  updated_website_url= request.POST['updated_website_url']
  updated_about_me= request.POST['updated_about_me']
 
  UserCurrent= users.objects.filter(id=dataIt[0])
  for x in UserCurrent:
    updated_data=x
    if(not updated_account_id):
      updated_data.account_id= updated_account_id
    if(not updated_display_name):
      updated_data.display_name= updated_display_name
    if(not updated_location):
      updated_data.location= updated_location
    if(not updated_profile_image_url):
      updated_data.profile_image_url= updated_profile_image_url
    if(not updated_website_url):
      updated_data.website_url= updated_website_url
    if(not updated_about_me):
      updated_data.about_me= updated_about_me
    updated_data.save()
    print(updated_data)
  
  return render(request, 'edited.html')


def home(request):
  # queries=
  return render(request, 'index.html')

def signin(request):

  if request.method=='POST':
    id=request.POST.get('accountid')
    pw=request.POST.get('pw')
    print(id,pw)
    curr_user=users.objects.filter(id=id)
    print(curr_user)
    if not curr_user:
      print("dsskjds")
      return HttpResponse("Check your credential")
    else:

      UserCurrent=users.objects.filter(id=id)
      #UserCurrent = [i for i in UserCurrent]  # converts ValuesQuerySet into Python list
      print(UserCurrent)
      listIt =[]
      for x in UserCurrent:
        listIt.append(x.id)
        listIt.append(x.account_id)
        listIt.append(x.reputation)
        listIt.append(x.views)
        listIt.append(x.down_votes)
        listIt.append(x.up_votes)
        listIt.append(x.display_name)
        listIt.append(x.location)
        listIt.append(x.profile_image_url)
        listIt.append(x.website_url)
        listIt.append(x.about_me)
        listIt.append(x.creation_date)
        listIt.append(x.last_access_date)
        global dataIt
        dataIt=listIt
      
      return render(request, 'index.html',{'user_id':listIt[0],'user_account_id':listIt[1],'user_reputation':listIt[2],'user_views':listIt[3],'user_down_views':listIt[4],'user_up_views':listIt[5],'user_display_name':listIt[6],'user_location':listIt[7],'user_profile_image_url':listIt[8],'user_website_url':listIt[9],'user_about_me':listIt[10],'user_creation_date':listIt[11],'user_last_access_date':listIt[12]})
  return render(request,'signin.html')

def signup(request):
  return render(request, 'signup.html')

def editProfile(request):
  listIt=dataIt
  return render(request, 'editProfile.html',{'user_id':listIt[0],'user_account_id':listIt[1],'user_reputation':listIt[2],'user_views':listIt[3],'user_down_views':listIt[4],'user_up_views':listIt[5],'user_display_name':listIt[6],'user_location':listIt[7],'user_profile_image_url':listIt[8],'user_website_url':listIt[9],'user_about_me':listIt[10],'user_creation_date':listIt[11],'user_last_access_date':listIt[12]})


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


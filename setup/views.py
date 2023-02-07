from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from setup.models import users, posts, comments
from django.contrib import auth
from datetime import datetime

dataIt=[423930,100,0,0,0,0,'pradeep','hyd',0,0,0,0,0]
parentID_for_AnswerPost=1
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
  queries= posts.objects.filter(post_type_id=1).order_by('-view_count')[:10]
  print(queries)
  return render(request, 'index.html',{'topPosts':list(queries.values())})

def eachpost(request):
  if request.method=='POST':
    id=request.POST.get('id')
    global parentID_for_AnswerPost
    parentID_for_AnswerPost=id
    answersList=list(posts.objects.filter(parent_id=id).values())
    # for i in range(len(answersList)):
    #   answersList[i]['index']=i

    ques=posts.objects.filter(id=id)

    # commentsList=[]
    for i in answersList:
      i['commentsList']=list(comments.objects.filter(post_id=i['id']).values())
    return render(request,'eachpost.html',{'ques':list(ques.values()),'answersList':answersList,})



def signin(request):

  if request.method=='POST':
    id=request.POST.get('id')
    pw=request.POST.get('display_name')
    currUser=users.objects.filter(id=id)
    if not currUser:
      return HttpResponse("Check your credential")
    else:    
      queries= posts.objects.filter(post_type_id=1).order_by('-view_count')[:10]

      return render(request, 'index.html',{'user':list(currUser.values()), 'topPosts':list(queries.values())})
  return render(request,'signin.html')


def signup(request):
  return render(request, 'signup.html')


def editProfile(request):
  listIt=dataIt
  return render(request, 'editProfile.html',{'user_id':listIt[0],'user_account_id':listIt[1],'user_reputation':listIt[2],'user_views':listIt[3],'user_down_views':listIt[4],'user_up_views':listIt[5],'user_display_name':listIt[6],'user_location':listIt[7],'user_profile_image_url':listIt[8],'user_website_url':listIt[9],'user_about_me':listIt[10],'user_creation_date':listIt[11],'user_last_access_date':listIt[12]})



#############
# MANAGE COOKIES
def manageCookies(request):
  return render(request,'manageCookies.html')
from django.shortcuts import render  
from django.http import HttpResponse  
  
def setcookie(request):  
    response = HttpResponse("Cookie Set")  
    response.set_cookie('java-tutorial', 'javatpoint.com')  
    return response  
def getcookie(request):  
    tutorial  = request.COOKIES['java-tutorial']  
    return HttpResponse("java tutorials @: "+  tutorial);  



def set_cookie(response, key, value):
    response.set_cookie(key,value)
    
def view(request):
    response = HttpResponse("hello")
    set_cookie(response, 'name', 'jujule')
    return response

# Check out template.html to see how the mymembers object
# was used in the HTML code. 
# Create your views here.
def search(request):
  if request.method=='POST':
    searchBy=request.POST.get('searchBy')
    searchValue=request.POST.get('searchValue')
    print(searchBy,searchValue)
    if searchBy=='userId':
      global relatedPostsList
      relatedPosts=posts.objects.filter(owner_user_id=searchValue)
      relatedPostsList=list(relatedPosts.values())

    elif searchBy=='tags':
      global searchValueList

      searchValueList=searchValue.split(' ')
      allPostsList=list(posts.objects.all().values())
      relatedPostsList=find_using_tags(allPostsList,searchValueList)



    if not relatedPostsList:
      return HttpResponse("no matches found")
    return render(request,'search.html',{'relatedPostsList':relatedPostsList,'searchValue':searchValue})


############
#  CREATE POST
def createPost(request):
  listIt=dataIt
  return render(request,'createPost.html',{'owner_user_id':listIt[0],'owner_display_name':listIt[6]})

def PostCreated(request):
  if request.method=='POST':
    lastRowById = posts.objects.all().order_by('id')[:1]
    CPid= 1+lastRowById['id']
    CPownerUserId=request.POST.get('OwnerUserId')
    CPownerDisplayName=request.POST.get('OwnerDisplayName')
    CPcreation_date=datetime.now()
    CPcontent_license="CC BY-SA 4.0"
    CPtitle=request.POST.get('createPostTitle')
    CPTags=request.POST.get('createPostTags')
    CPBody=request.POST.get('createPostBody')
    
    # Upload data in posts table
    new_CreatePost=posts(id=CPid,owner_user_id=CPownerUserId,last_editor_user_id=None,
	post_type_id=1,accepted_answer_id=None,score=0,parent_id=0,view_count=0,answer_count=0,comment_count=0,owner_display_name=CPownerDisplayName,
	last_editor_display_name =None,title =CPtitle,tags =CPTags,	content_license=CPcontent_license,body=CPBody,favorite_count=None,
  creation_date =CPcreation_date,	community_owned_date=None,	closed_date=None,	last_edit_date=None,	last_activity_date=CPcreation_date)
    new_CreatePost.save()
    print(new_CreatePost)
    # Upload data in postHistory(later)


# -- select real_id from (select T.id as real_id from setup_posts as S, setup_posts as T where T.post_type_id=1 and S.id=T.id and T.owner_user_id=S.last_editor_user_id);

# select * from setup_post_history where post_id=26264;

# -- 134 724

# -- select A.real_id,count(*) from setup_post_history as B, (select T.id as real_id from setup_posts as S, setup_posts as T where T.post_type_id=1 and S.id=T.id and T.owner_user_id=S.last_editor_user_id) as A where A.real_id=B.post_id group by A.real_id having count(*)<4
# -- select post_id from setup_post_history as B where post_history_type_id=1 or post_history_type_id=2 or post_history_type_id=3 group by post_id having count(*)=3

    return render(request, 'YourPost.html', {'CreatedPost':new_CreatePost,'owner_user_id':dataIt[0],'owner_display_name':dataIt[6]})



################################

def  PostAnswer(request):
  if request.method=='POST':
    ques=posts.objects.filter(id=parentID_for_AnswerPost)
    return render(request,'PostAnswer.html',{'ques':list(ques.values()),'owner_user_id':dataIt[0],'owner_display_name':dataIt[6]})


def AnsweredPost(request):
   if request.method=='POST':
    postIdGeneration = posts.objects.all().values()
    leng=len(postIdGeneration)
    CPid= 1+postIdGeneration[leng-1]['id']
    from datetime import datetime
    Current_timestamp=datetime.now()
    CPcontent_license="CC BY-SA 4.0"
    CPtitle=request.POST.get('createPostTitle')
    CPTags=request.POST.get('createPostTags')
    CPBody=request.POST.get('createPostBody')
    CPowner_user_id=dataIt[0]
    CPowner_display_name=dataIt[6]
    # Upload data in posts table
    new_AnswerPost=posts(id=CPid,owner_user_id=CPowner_user_id,last_editor_user_id=None,
	post_type_id=2,accepted_answer_id=None,score=0,parent_id=parentID_for_AnswerPost,view_count=0,answer_count=0,comment_count=0,owner_display_name=CPowner_display_name,
	last_editor_display_name =None,title =CPtitle,tags =CPTags,	content_license=CPcontent_license,body=CPBody,favorite_count=None,
  creation_date =Current_timestamp,	community_owned_date=None,	closed_date=None,	last_edit_date=None,	last_activity_date=Current_timestamp)
    new_AnswerPost.save()
    # Update the quesion/ create post thing
    ParentIt=posts.objects.filter(id=parentID_for_AnswerPost).values()
    print(ParentIt[0]['answer_count'])
    current_answer_count= ParentIt[0]['answer_count']+1
    posts.objects.filter(id=parentID_for_AnswerPost).update(answer_count=current_answer_count)
    print(new_AnswerPost)
    # Upload data in postHistory(later)



    return render(request, 'AnsweredPost.html', {'AnswerPost':new_AnswerPost})


def AllYourPosts(request):
      postsAll=posts.objects.filter(owner_user_id=49553)
      postsAll=list(postsAll.values())
      print(len(postsAll))
      return render(request,'AllYourPosts.html',{'postsAll':postsAll})

###########

def find(tag, str):
    """ A helper function which will helps in finding 
        if a tag is present in a list of tags 
        of the form  "<tag1> <tag2> ... " 
        Returns True if present
                                            """
    if not str:
      return False                                     
    tag_list = str[1:-1].split('><')
    if(tag in tag_list):
        return True
         
    return False


def find_using_tags(d , tags):
    """
        Arguments: d = list of dictionaries,
               *tags = variable number of tags which the user is searching for
    
    Function to print all the rows in the list of dict
    which contains all the tags which the user is searching for(intersection)
    """
    is_present = False
    temp_list=[]
    for i in range(len(d)):

        for tag in tags:
            if(find(tag, d[i]['tags'])):
                is_present = True
            else:
                is_present = False
                break
        if(is_present):
          temp_list.append(d[i])
    return temp_list



def find_using_xyz(d, attribute, value):
    """ Function to print all the rows in the list 
        of dicts which contains the value which the user 
        is searching for according to the attribute he/she chose. 
        """
    tempList=[]                                                             
    for i in range(len(d)):
        if(d[i][attribute] == value):
            tempList.append(d[i])
    return tempList


# Sample list of dictionaries
d = [{'id': 1, 'owner_id': 8802, 'tags': "<python> <c++>"}, 
{'id': 2, 'owner_id': 123, 'tags': "<python> <c>"}, 
{'id': 3, 'owner_id': 1234, 'tags': "<javascript> <cp>"}, 
{'id': 4, 'owner_id': 1234, 'tags': "<java> <c#>"}, 
{'id': 5, 'owner_id': 1234, 'tags': "<django> <flask>"}, 
{'id': 6, 'owner_id': 1234, 'tags': "<python> <latex>"},
{'id': 7, 'owner_id': 211, 'tags': "<c--> <c++>"}, 
{'id': 8, 'owner_id': 211, 'tags': "<python> <cpp>"}]

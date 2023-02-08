from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from setup.models import users, posts, comments
from django.contrib import auth
from datetime import datetime
from django.contrib import messages
# from django.utils.safestring import mark_safe

def signup(request):
  if request.method=='POST':

    lastRowById = list(users.objects.all().order_by('-id')[:1].values())

    newId= 1+lastRowById[0]['id']
    print(newId)
    new_account_id=request.POST.get('account_id')
    new_reputation=0
    new_views=0
    new_down_votes=0
    new_up_votes=0
    new_display_name=request.POST.get('display_name')
    newCreationDate=datetime.now()
    newLastAccessDate=datetime.now()

    new_location=request.POST.get('location')
    new_about_me=request.POST.get('about_me')
    new_fellow=users(id=newId,account_id=new_account_id,reputation=new_reputation,views=new_views,down_votes=new_down_votes,up_votes=new_up_votes,display_name=new_display_name,location=new_location,about_me=new_about_me,creation_date=newCreationDate, last_access_date=newLastAccessDate)
    
    new_fellow.save()
    # print(new_fellow)
    new_fellow=users.objects.filter(id=newId)
    queries= posts.objects.filter(post_type_id=1).order_by('-view_count')[:10]
    response=render(request, 'index.html',{'user':list(new_fellow.values()), 'topPosts':list(queries.values())})
    response.set_cookie('userId',newId)
    response.set_cookie('loginStatus',True)
    return response
  return render(request, 'signup.html')


def profileEdited(request):
# if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
  id=request.COOKIES['userId']
  updated_account_id= request.POST['updated_account_id']
  updated_display_name = request.POST['updated_display_name']
  updated_location= request.POST['updated_location']
  updated_profile_image_url= request.POST['updated_profile_image_url']
  updated_website_url= request.POST['updated_website_url']
  updated_about_me= request.POST['updated_about_me']
 
  currUser= users.objects.get(id=id)

  currUser.account_id= updated_account_id
  currUser.display_name= updated_display_name
  currUser.location= updated_location
  currUser.profile_image_url= updated_profile_image_url
  currUser.website_url= updated_website_url
  currUser.about_me= updated_about_me
  currUser.save()
  print(currUser)
  
  return home(request)

# logout function
def logout(request):
  queries= list(posts.objects.filter(post_type_id=1).order_by('-view_count')[:10].values())
  response=render(request,'index.html',{'topPosts':queries})
  response.delete_cookie('userId')
  response.delete_cookie('loginStatus')
  return response

# home page
def home(request):
  queries= list(posts.objects.filter(post_type_id=1).order_by('-view_count')[:10].values())

  if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
    currUserId=request.COOKIES['userId']
    currUserList=list(users.objects.filter(id=currUserId).values())
    return render(request, 'index.html',{'user':currUserList, 'topPosts':queries})
  return render(request, 'index.html',{'topPosts':queries})


def signin(request):

  if request.method=='POST':
    id=request.POST.get('id')
    pw=request.POST.get('display_name')
    currUser=users.objects.filter(id=id)

    if not currUser:
      return HttpResponse("Check your credential")
    else:
      queries= posts.objects.filter(post_type_id=1).order_by('-view_count')[:10]
      response=render(request, 'index.html',{'user':list(currUser.values()), 'topPosts':list(queries.values())})
      response.set_cookie('userId',list(currUser.values())[0]['id'])
      response.set_cookie('loginStatus',True)
      return response
  return render(request,'signin.html')


  



def eachpost(request):
  messages.success(request, "Post Created")
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






def editProfile(request):
  if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
    currUserId=request.COOKIES['userId']
    currUser=list(users.objects.filter(id=currUserId).values())[0]
    return render(request, 'editProfile.html',{'user':currUser})
  else:
    return HttpResponse("first login dude")



# Check out template.html to see how the mymembers object
# was used in the HTML code. 
# Create your views here.
def search(request):
  if request.method=='POST':
    searchBy=request.POST.get('searchBy')
    searchValue=request.POST.get('searchValue')
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
#  CREATE POST PAGE
def createPost(request):
  if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
    return render(request,'createPost.html')
  return HttpResponse('first login bro')

############
# UPDATING POST TO DATABASE
def PostCreated(request):
  if request.method=='POST':
    
    if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:

      lastRowById = list(posts.objects.all().order_by('id')[:1].values())
      CPid= 1+lastRowById[0]['id']
      CPownerUserId=request.COOKIES['userId']

      ownerUser=list(users.objects.filter(id=CPownerUserId).values())

      CPpostTypeId=1
      CPownerDisplayName=ownerUser['display_name']
      CPcommentCount=0
      CPanswerCount=0
      CPcreationDate=datetime.now()
      CPcontent_license="CC BY-SA 4.0"
      CPtitle=request.POST.get('createPostTitle')
      CPTags=request.POST.get('createPostTags')
      CPBody=request.POST.get('createPostBody')
      
      # Upload data in posts table
      new_CreatePost=posts(id=CPid, owner_user_id=CPownerUserId, post_type_id=1, score=0, view_count=0, answer_count=0, comment_count=0, owner_display_name=CPownerDisplayName,title =CPtitle,tags =CPTags,	content_license=CPcontent_license,body=CPBody, creation_date =CPcreationDate,last_activity_date=CPcreationDate)
      new_CreatePost.save()
      print(new_CreatePost)
      new_CreatePostList=list(new_CreatePost.values())
      messages.success(request, "Post Created")
      return render(request,'eachpost',{'newPost':new_CreatePostList})
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

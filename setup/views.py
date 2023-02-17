import re
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
parentID_for_AnswerPost=0
from setup.models import *
from django.contrib import auth
import json
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
# relatedPostsData=posts.objects.filter(post_type_id=1)
# from django.utils.safestring import mark_safe

# filter of upvotes and time:
# def OrderByUpvotes(request):
#   #queriesOrder= posts.objects.filter(post_type_id=1).order_by('creation_date')[:10]
  
#   all_tags = list(tags.objects.values_list('tag_name',flat = True))
#   all_user_names = list(users.objects.values_list('display_name',flat = True))
#   queriesOrder=relatedPostsData.order_by('-creation_date')
#   queriesOrder=relatedPostsData.order_by('-creation_date')
  
#   #request.POST.get('upvotesSort')
#   # print(type(queriesOrder))
#   queriesOrder=queriesOrder #.order_by('creation_date')
#   print(queriesOrder)
#   queriesOrder=list(queriesOrder.values())

#   if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
#     currUserId=request.COOKIES['userId']
#     currUser=list(users.objects.filter(id=currUserId).values())
#     rs_dict = {'topPosts':queriesOrder}
#   else:
#     rs_dict = {'topPosts':queriesOrder}
#   return render(request, 'search.html', {'relatedPostsList':queriesOrder,'avail_tags':all_tags,'avail_users':all_user_names})


def signup(request):
  if request.method=='POST':

    lastRowById = list(users.objects.all().order_by('-id')[:1].values())

    newId= 1+lastRowById[0]['id']
    print(newId)
    new_account_id=request.POST.get('account_id')
    new_reputation=0
    new_views=0
    # new_down_votes=0
    # new_up_votes=0
    new_display_name=request.POST.get('display_name')
    newCreationDate=datetime.now()
    newLastAccessDate=datetime.now()
    new_location=request.POST.get('location')
    new_about_me=request.POST.get('about_me')
    new_fellow=users(id=newId,account_id=new_account_id,reputation=new_reputation,views=new_views,down_votes=new_down_votes,up_votes=new_up_votes,display_name=new_display_name,location=new_location,about_me=new_about_me,creation_date=newCreationDate, last_access_date=newLastAccessDate)
    
    new_fellow.save()
    new_fellow=users.objects.filter(id=newId)

    response=HttpResponseRedirect('/')
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
  
  return HttpResponseRedirect('/')

# logout function
def logout(request):
  response=HttpResponseRedirect('/')
  response.delete_cookie('userId')
  response.delete_cookie('loginStatus')
  return response


# home page
def home(request):
  queries= posts.objects.filter(post_type_id=1).order_by('-view_count')[:10]
  # global relatedPostsData
  # relatedPostsData= posts.objects.filter(post_type_id=1)
  all_tags = list(tags.objects.values_list('tag_name',flat = True))
  all_user_names = list(users.objects.values_list('display_name',flat = True))
  if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
    currUserId=request.COOKIES['userId']
    currUser=list(users.objects.filter(id=currUserId).values())
    rs_dict = {'topPosts':list(queries.values()),'avail_tags':all_tags,'avail_users':all_user_names,'user':currUser}
  else:
    rs_dict = {'topPosts':list(queries.values()),'avail_tags':all_tags,'avail_users':all_user_names}
  return render(request, 'index.html', rs_dict)


def eachpost(request):  
  if request.method == 'POST':
    id=request.POST.get('id')

    answersList=list(posts.objects.filter(parent_id=id).values())
    for i in range(len(answersList)):
      answersList[i]['index']=i
    ques=posts.objects.filter(id=id)
    commentsList = [
        list(comments.objects.filter(post_id=i['id']).values())
        for i in answersList
    ]
    if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
      currUserId=request.COOKIES['userId']
      currUser=list(users.objects.filter(id=currUserId).values())
      currDict={'ques':list(ques.values()),'answersList':answersList, 'commentsList':commentsList,'user':currUser}
    else:
      currDict={'ques':list(ques.values()),'answersList':answersList, 'commentsList':commentsList}
    return render(request,'eachpost.html',currDict)


def signin(request):

  if request.method=='POST':
    id=request.POST.get('id')
    pw=request.POST.get('display_name')
    currUser=users.objects.filter(id=id)

    if not currUser:
      messages.error(request, "Check your credentials")
      return HttpResponseRedirect('/signin')
      
    else:
      response=HttpResponseRedirect('/')
      response.set_cookie('userId',list(currUser.values())[0]['id'])
      response.set_cookie('loginStatus',True)
      return response
  return render(request,'signin.html')







def editProfile(request):
  if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
    currUserId=request.COOKIES['userId']
    currUser=list(users.objects.filter(id=currUserId).values())[0]
    return render(request, 'editProfile.html',{'user':currUser})
  else:
    messages.error(request, 'First you have to login')
    return HttpResponseRedirect('/')



# Check out template.html to see how the mymembers object
# was used in the HTML code. 
# Create your views here.
def search(request):
  if request.method=='POST':
    searchBy=request.POST.get('searchBy')
    searchValue=request.POST.get('searchValue')
    if searchBy=='username':
      global relatedPostsList
      print(searchValue)
      relatedPosts=posts.objects.filter(owner_display_name=searchValue)
      global relatedPostsData
      relatedPostsData=relatedPosts
      relatedPostsList=list(relatedPosts.values())


    elif searchBy=='tags':
      global searchValueList

      searchValueList=searchValue.split(' ')
      allPostsList=list(posts.objects.all().values())
      relatedPostsList=find_using_tags(allPostsList,searchValueList)



    if not relatedPostsList:
      messages.error(request, "No matches found")
      return HttpResponseRedirect('/')

    return render(request,'search.html',{'relatedPostsList':relatedPostsList,'searchValue':searchValue})


############
#  CREATE POST PAGE
def createPost(request):
  if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
    currUserId=request.COOKIES['userId']
    owner_display_name=users.objects.filter(id=currUserId).values()
    owner_display_name=owner_display_name[0]['display_name']
    return render(request,'createPost.html',{'owner_user_id':currUserId,'owner_display_name':owner_display_name})
  messages.info(request, "You have to login for creating posts")
  print("yes")
  if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
    currUserId=request.COOKIES['userId']
  return render(request,'signin.html')

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
    #print(ParentIt[0]['answer_count'])
    current_answer_count= ParentIt[0]['answer_count']+1
    posts.objects.filter(id=parentID_for_AnswerPost).update(answer_count=current_answer_count)
    #print(new_AnswerPost)
    # Upload data in postHistory(later)



    return render(request, 'AnsweredPost.html', {'AnswerPost':new_AnswerPost})

def Singlepost(request):
  
  owner_user_id_ForEditingPosts=160
  if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
    owner_user_id_ForEditingPosts=request.COOKIES['userId']
    output=request.POST.get('submit')
    id=request.POST.get('id')
    if(output=="Edit"):
      global PostData
      PostData=posts.objects.filter(id=id,owner_user_id=owner_user_id_ForEditingPosts).values()
      print(PostData)
      return render(request, 'editYourPost.html', {'postdata':PostData,'owner_user_id':owner_user_id_ForEditingPosts,'id':id})

    return render(request, 'eachPost.html')


def AllYourPosts(request):
  
      if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
        currUserId=request.COOKIES['userId']
        allPosts=list(posts.objects.filter(owner_user_id=currUserId).values())
        user=list(users.objects.filter(id=currUserId).values())
        if len(allPosts)>0:
          return render(request,'AllYourPosts.html',{'postsAll':allPosts,"user":user})
        messages.info(request, "You haven't created any posts")
        return HttpResponseRedirect('/')
      messages.error(request, "First you have to login")
      return HttpResponseRedirect('/')



def PostEdited(request):  
  # currentPostId=PostData['id']
  ToDo=request.POST.get('EditIt')
  EPId=request.POST.get('ThePostaData')
  print(ToDo)
  if(ToDo=='2'):
            print("Bro it is deleted")
            posts.objects.filter(id=EPId).delete()
  else:          
    EPTitle=request.POST.get('EditedPostTitle')
    EPTags=request.POST.get('EditedPostTags')
    EPContent_license=request.POST.get('EditedPostcontent_license')
    EPBody=request.POST.get('EditedPostBody')
    EPId=request.POST.get('ThePostaData')
    EPlast_edit_date=datetime.now()
    # TotalData=request.POST.get('TotalPostData')
    posts.objects.filter(id=EPId).update(tags=EPTags,title=EPTitle,body=EPBody,content_license=EPContent_license,last_edit_date=EPlast_edit_date)
    TotalData=posts.objects.filter(id=EPId).values()
  return render(request,'EditedPostPage.html')
   
def CommentAdded(request):
    ThePostId=request.POST.get('PostId')
    ThePostContent_license=request.POST.get('ThePostContent_license')
    # user_id=request.POST.get('user_id')
    Bodytext=request.POST.get('Bodytext')
    currUserId=0
    print(ThePostId)
    if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
      currUserId=request.COOKIES['userId']
     # owner_display_name=users.objects.filter(id=currUserId).values()
    #  owner_display_name=owner_display_name[0]['display_name']
    
    print(currUserId)
    # Updated the comments table here
    CommentWriter= users.objects.filter(id=currUserId).values()
    CommentWriter=CommentWriter[0]['display_name']
    # getting user_display_name from users table
    CoomentIdGeneration = comments.objects.all().values()
    leng=len(CoomentIdGeneration)
    CId= 1+CoomentIdGeneration[leng-1]['id']
    Ccreation_date=datetime.now()
    new_comment=comments(id=CId, post_id=ThePostId, user_id=currUserId, score=0, content_license=ThePostContent_license, user_display_name=CommentWriter,text=Bodytext,creation_date =Ccreation_date)
    new_comment.save()

    # Updated the posts table here
    a=request.POST.get('ThePostcomment_count')
    print(a,"fkskfs")

    ThePostcomment_count=1+int(a)
    Clast_activity_date=datetime.now()
    posts.objects.filter(id=ThePostId).update(comment_count=ThePostcomment_count,last_activity_date=Clast_activity_date)
    print("The shit of comment adding is done")
    
    return HttpResponseRedirect('/')
###########
def AddComment(request):
  v=request.POST.get('AboutPostData')
  ThePostId=int(v)
  ThePost=list(posts.objects.filter(id=ThePostId).values())[0]
  # print(ThePost)
  user_id=000
  if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
      user_id=request.COOKIES['userId']
  return render(request,'CommentPage.html',{'PostData':ThePost,'user_id':user_id})



#################
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
  return [d[i] for i in range(len(d)) if (d[i][attribute] == value)]


# def findTheUpvoteVoteCount(UpVotes,keyIt):
#   return UpVotes[keyIt]
# Sample list of dictionaries
d = [{'id': 1, 'owner_id': 8802, 'tags': "<python> <c++>"}, 
{'id': 2, 'owner_id': 123, 'tags': "<python> <c>"}, 
{'id': 3, 'owner_id': 1234, 'tags': "<javascript> <cp>"}, 
{'id': 4, 'owner_id': 1234, 'tags': "<java> <c#>"}, 
{'id': 5, 'owner_id': 1234, 'tags': "<django> <flask>"}, 
{'id': 6, 'owner_id': 1234, 'tags': "<python> <latex>"},
{'id': 7, 'owner_id': 211, 'tags': "<c--> <c++>"}, 
{'id': 8, 'owner_id': 211, 'tags': "<python> <cpp>"}]

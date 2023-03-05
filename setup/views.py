import re
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from setup.models import *
from django.db import models
from django.forms.models import model_to_dict
from django.db.models import F
from django.contrib import auth
import json
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.http import HttpResponseNotAllowed
# relatedPostsData=posts.objects.filter(post_type_id=1)
# from django.utils.safestring import mark_safe

# filter of upvotes and time:
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
    new_fellow=users.objects.filter(id=newId)

    response=HttpResponseRedirect('/')
    response.set_cookie('userId',newId)
    response.set_cookie('loginStatus',True)
    return response

  return render(request, 'signup3.html')


def profileEdited(request):
# if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
  id=request.COOKIES['userId']
  # updated_account_id= request.POST['updated_account_id']
  updated_display_name = request.POST['updated_display_name']
  updated_location= request.POST['updated_location']
  updated_profile_image_url= request.POST['updated_profile_image_url']
  updated_website_url= request.POST['updated_website_url']
  updated_about_me= request.POST['updated_about_me']
 
  currUser= users.objects.get(id=id)

  # currUser.account_id= updated_account_id
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

  all_tags = list(tags.objects.values_list('tag_name',flat = True))
  all_user_names = list(users.objects.values_list('display_name',flat = True))
  if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
    currUserId=request.COOKIES['userId']
    currUser=list(users.objects.filter(id=currUserId).values())
    rs_dict = {'topPosts':list(queries.values()),'avail_tags':all_tags,'avail_users':all_user_names,'user':currUser[0]}
  else:
    rs_dict = {'topPosts':list(queries.values()),'avail_tags':all_tags,'avail_users':all_user_names}
  return render(request, 'index.html', rs_dict)


def eachpost(request): 
  
  if request.method=='GET':
    id=request.GET.get('quesId')
    answersList=list(posts.objects.filter(parent_id=id).order_by('-score').values())
    # print(answersList[0])
    for i in range(len(answersList)):
      answersList[i]['index']=i
    ques=posts.objects.filter(id=id)
    quesComments=list(comments.objects.filter(post_id=id).order_by('id').values())
    # print(quesComments)
    # quesComments_name =  users.objects.filter(id = )
    for i in answersList:
      i['commentsList']=list(comments.objects.filter(post_id=i['id']).order_by('id').values())

    if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
      currUserId=request.COOKIES['userId']
      currUser=list(users.objects.filter(id=currUserId).values())[0]
      currDict={'ques':list(ques.values()),'quesComments':quesComments,'answersList':answersList, 'user':currUser}
    else:
      currDict={'ques':list(ques.values()),'quesComments':quesComments,'answersList':answersList}
    return render(request,'eachpost.html',currDict)

def Votes_Update(request):
    if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
       if request.method == 'POST':
         post_id = request.POST.get('id')
         direction = request.POST.get('direction')
         obj = posts.objects.get(id=post_id)
         currScore = obj.score
         if direction == 'up':
           newScore = currScore + 1
         elif direction == 'down':
           newScore = currScore -1
         obj.score = newScore
         obj.save()
         return JsonResponse({'newScore':newScore})
    # else :
    #   messages.error(request, 'Only users can upvote/downvote a post')  
    #   return HttpResponseRedirect('/signin')
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

def editPost(request):
  if request.method=='POST':
    currPostId=request.POST['postId']
    currUserId=request.COOKIES['userId']
    currUser=list(users.objects.filter(id=currUserId).values())[0]
    currPost=posts.objects.filter(id=currPostId).values()[0]
    all_tags = list(tags.objects.values_list('tag_name',flat = True))
    return render(request,'editPost.html',{'post':currPost, 'user':currUser,'avail_tags':all_tags})
  

def postEdited(request):
    if request.method=='POST':
      
      currPostId=request.POST.get('postId')
      currPost= posts.objects.get(id=currPostId)
      if currPost.post_type_id==1:
        CPtitle=request.POST.get('createPostTitle')
        CPTags=request.POST.get('createPostTags')
        currPost.title=CPtitle
        currPost.tags=CPTags
      CPBody=request.POST.get('createPostBody')  
      print(CPBody)
      currPost.body=CPBody
      currPost.last_activity_date=datetime.now()

      currPost.save()

      messages.success(request,"post edited")
      return HttpResponseRedirect('/AllYourPosts')

def deletePost(request):
  if request.method=='POST':
    currPostId=request.POST.get('postId')
    currPost= posts.objects.get(id=currPostId)
    currPost.delete()

    messages.success(request,"post deleted")
    return HttpResponseRedirect('/AllYourPosts')



      






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
    searchValue=request.POST.get('searchValue')  # himashu/ syntax, cp
    sortBy=request.POST.get('sortBy')     # date/upvotes
    if searchBy=='username':
      global relatedPostsList
      
      if sortBy == 'date':
        relatedPosts=posts.objects.filter(owner_display_name=searchValue).order_by('-creation_date')
      elif sortBy == 'upvotes':
        relatedPosts=posts.objects.filter(owner_display_name=searchValue).order_by('-score')
      
      global relatedPostsData
      relatedPostsData=relatedPosts
      relatedPostsList=list(relatedPosts.values())


    elif searchBy=='tags':
      global searchValueList

      searchValueList=searchValue.split(' ')
      if sortBy == 'date':
        allPostsList=list(posts.objects.all().order_by('-creation_date').values())
      elif sortBy == 'upvotes':
        allPostsList=list(posts.objects.all().order_by('-score').values())


      relatedPostsList=find_using_tags(allPostsList,searchValueList)



    if not relatedPostsList:
      messages.error(request, "No matches found")
      return HttpResponseRedirect('/')
    all_tags = list(tags.objects.values_list('tag_name',flat = True))
    all_user_names = list(users.objects.values_list('display_name',flat = True))
    return render(request,'search.html',{'relatedPostsList':relatedPostsList,'searchValue':searchValue,'avail_tags':all_tags,'avail_users':all_user_names})


############
#  CREATE POST PAGE
def createPost(request):
  if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
    currUserId=request.COOKIES['userId']
    currUser=users.objects.filter(id=currUserId).values()[0]
    all_tags = list(tags.objects.values_list('tag_name',flat = True))
    return render(request,'createPost.html',{'user':currUser,'avail_tags':all_tags})
  messages.info(request, "You have to login for creating posts")

  return HttpResponseRedirect('/signin')

############
# UPDATING POST TO DATABASE
def PostCreated(request):
  if request.method=='POST':
    
    if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:

      lastRowById = list(posts.objects.all().order_by('-id')[:1].values())
      CPid= 1+lastRowById[0]['id']
      CPownerUserId=request.COOKIES['userId']
      ownerUser=users.objects.get(id=CPownerUserId)
      CPownerDisplayName=ownerUser.display_name
 
      CPcreationDate=datetime.now()
      CPcontent_license="CC BY-SA 4.0"
      CPtitle=request.POST.get('createPostTitle')
      CPTags=request.POST.get('createPostTags')
      CPBody=request.POST.get('createPostBody')
      
      # Upload data in posts table
      new_CreatePost=posts(id=CPid, owner_user_id=ownerUser, post_type_id=1, score=0, view_count=0, answer_count=0, comment_count=0, owner_display_name=CPownerDisplayName,title =CPtitle,tags =CPTags,	content_license=CPcontent_license,body=CPBody, creation_date =CPcreationDate,last_activity_date=CPcreationDate)
      new_CreatePost.save()
      new_CreatePost=model_to_dict(new_CreatePost)
      messages.success(request, "Post Created")
      return HttpResponseRedirect('/')
      # return render(request,'eachpost',{'newPost':new_CreatePost,'user':model_to_dict(ownerUser)})



################################

def  PostAnswer(request):
  if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
    currUserId=request.COOKIES['userId']
    # if request.method=='POST':
    currUser=list(users.objects.filter(id=currUserId).values())[0]
    quesId=request.POST.get('quesId')
    print(quesId)
    return render(request,'PostAnswer.html',{'quesId':quesId,'user':currUser})

  messages.info(request, "You have to login for answering post")

  return render(request,'signin.html')



def AnsweredPost(request):
   if request.method=='POST':
    # if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:

    currUserId=request.COOKIES['userId']
    ownerUser=users.objects.get(id=currUserId)
    curruserName=ownerUser.display_name
    lastRowById = list(posts.objects.all().order_by('-id')[:1].values())
    CPid= 1+lastRowById[0]['id']
    CPcontent_license="CC BY-SA 4.0"

    currQuesId=request.POST.get('postAnswerQuesId')
    currBody=request.POST.get('postAnswerBody')
    print(currUserId)

    new_AnswerPost=posts(id=CPid,owner_user_id=ownerUser, post_type_id=2, score=0,parent_id=currQuesId,view_count=0,answer_count=0,comment_count=0,owner_display_name=curruserName,
	content_license=CPcontent_license,body=currBody, creation_date =datetime.now(),last_activity_date=datetime.now())
    new_AnswerPost.save()
    print(currUserId)
    # Update the quesion/ create post thing
    ParentIt=posts.objects.filter(id=currQuesId).values()
    current_answer_count= ParentIt[0]['answer_count']+1
    posts.objects.filter(id=currQuesId).update(answer_count=current_answer_count)

    # Upload data in postHistory(later)


    response=HttpResponseRedirect('/eachpost?quesId='+currQuesId)
    # return render(request, 'AnsweredPost.html', {'AnswerPost':new_AnswerPost})
    messages.success(request,'Answer Created')
    return response

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

def profile(request):
  if not 'userId' in request.COOKIES:
    response=HttpResponseRedirect('/')
    messages.error(request,'You can\'t access this page')
    return response
  currUserId=request.COOKIES['userId']
  currUser=users.objects.filter(id=currUserId).values()[0]
  # print(currUser,currUser.id)
  return render(request, 'profile.html',{'user':currUser})
  


def AllYourPosts(request):
  
      if 'loginStatus' in request.COOKIES and 'userId' in request.COOKIES:
        currUserId=request.COOKIES['userId']
        allPosts=list(posts.objects.filter(owner_user_id=currUserId).values())
        user=list(users.objects.filter(id=currUserId).values())[0]
        if len(allPosts)>0:
          return render(request,'AllYourPosts.html',{'allPosts':allPosts,"user":user})
        messages.info(request, "You haven't created any posts")
        return HttpResponseRedirect('/')
      messages.error(request, "First you have to login")
      return HttpResponseRedirect('/')



# def PostEdited(request):  
#   ToDo=request.POST.get('EditIt')
#   EPId=request.POST.get('ThePostaData')
#   print(ToDo)
#   if(ToDo=='2'):
#             print("Bro it is deleted")
#             posts.objects.filter(id=EPId).delete()
#   else:          
#     EPTitle=request.POST.get('EditedPostTitle')
#     EPTags=request.POST.get('EditedPostTags')
#     EPContent_license=request.POST.get('EditedPostcontent_license')
#     EPBody=request.POST.get('EditedPostBody')
#     EPId=request.POST.get('ThePostaData')
#     EPlast_edit_date=datetime.now()
#     posts.objects.filter(id=EPId).update(tags=EPTags,title=EPTitle,body=EPBody,content_license=EPContent_license,last_edit_date=EPlast_edit_date)
#     TotalData=posts.objects.filter(id=EPId).values()
#   return render(request,'EditedPostPage.html')
   
def CommentAdded(request):
    if request.method=='POST':
      gotPostId=request.POST.get('PostId')
      gotPost=posts.objects.get(id=gotPostId)
      ThePostContent_license="CC BY-SA 4.0"
      commentBody=request.POST.get('Bodytext')
      if not 'userId' in request.COOKIES:
        response=HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        messages.error(request,'You have to login for writing comments')
        return response
      currUserId=request.COOKIES['userId']
      
      currUser= users.objects.filter(id=currUserId).values() 
      currUser2=users.objects.get(id=currUserId)
      currUsername=currUser[0]['display_name']
      CoomentIdGeneration = comments.objects.all().values()
      leng=len(CoomentIdGeneration)
      CId= 1+CoomentIdGeneration[leng-1]['id']
      new_comment=comments(id=CId, post_id=gotPost, user_id=currUser2, score=0, content_license=ThePostContent_license, user_display_name=currUsername,text=commentBody,creation_date =datetime.now())
      new_comment.save()

      posts.objects.filter(id=gotPostId).update(comment_count=F('comment_count') + 1)
      posts.objects.filter(id=gotPostId).update(last_activity_date=datetime.now())

      response=HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      messages.success(request,'Comment Added')
      return response
    response=HttpResponseRedirect('/')
    messages.error(request,'You can\'t acces this page')
    return response


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

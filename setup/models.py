from django.db import models
import uuid



class users(models.Model):
    id=models.IntegerField(("id"),primary_key=True)
    account_id=models.IntegerField(("account_id"),null=True)
    reputation=models.IntegerField(("reputation"), null=False)
    views=models.IntegerField(("views"), default = 0)
    down_votes=models.IntegerField(("down_votes"), default = 0)
    up_votes=models.IntegerField(("up_votes"), default = 0,)
    display_name=models.CharField(("display_name"),max_length=255,null=False)
    location=models.CharField(("location"),max_length=512,null=True)
    profile_image_url=models.CharField(("profile_image_url"),max_length=255,null=True)
    website_url=models.CharField(("website_url"),max_length=255,null=True)
    about_me=models.TextField(("about_me"),null=True)
    creation_date=models.DateTimeField(("creation_date"),auto_now_add=True,null=False)
    last_access_date=models.DateTimeField(("last_access_date"),auto_now_add=True,null=False)

class posts(models.Model):
    id=models.IntegerField(("id"),primary_key=True)
    # owner_user_id=models.IntegerField(("owner_user_id"), null=True)
    owner_user_id= models.ForeignKey(users,related_name = 'owner_user_id',on_delete = models.SET('Anonymous'))
    # last_editor_user_id=models.IntegerField(("last_editor_user_id"),null=True)
    last_editor_user_id= models.ForeignKey(users,related_name = 'last_editor_user_id',on_delete = models.SET('Anonymous'))
    post_type_id=models.SmallIntegerField(("post_type_id"), null=False)
    accepted_answer_id=models.IntegerField(("accepted_answer_id"),null=True)
    score=models.IntegerField(("score"), null=False)
    parent_id=models.IntegerField(("parent_id"),null=True)
    view_count=models.IntegerField(("view_count"), null=True)
    answer_count=models.IntegerField(("answer_count"), default = 0, null=True)
    comment_count=models.IntegerField(("comment_count"), default = 0)
    owner_display_name=models.CharField(("owner_display_name"),max_length=64,null=True)
    last_editor_display_name=models.CharField(("last_editor_display_name"),max_length=64,null=True)
    title=models.CharField(("title"),max_length=512, null=True)
    tags=models.CharField(("tags"),max_length=512, null=True)
    content_license=models.CharField(("content_license"),max_length=64, null=False)
    body=models.TextField(("body"), null=True)
    favorite_count=models.IntegerField(("favorite_count"),null=True)
    creation_date=models.DateTimeField(("creation_date"),auto_now_add=True,null=False)
    community_owned_date=models.DateTimeField(("community_owned_date"),auto_now_add=True, null=True)
    closed_date=models.DateTimeField(("closed_date"),auto_now_add=True, null=True)
    last_edit_date=models.DateTimeField(("last_edit_date"),auto_now_add=True, null=True)
    last_activity_date=models.DateTimeField(("last_activity_date"),auto_now_add=True)

class tags(models.Model):
    id=models.IntegerField(("id"),primary_key=True)
    # excerpt_post_id=models.IntegerField(("excerpt_post_id"),null=True)
    excerpt_post_id = models.ForeignKey(posts,related_name = 'excerpt_post_id',on_delete = models.PROTECT)
    # wiki_post_id=models.IntegerField(("wiki_post_id"),null=True)
    wiki_post_id = models.ForeignKey(posts,related_name = 'wiki_post_id',on_delete = models.PROTECT)
    tag_name=models.CharField(("tag_name"),max_length=255,null=False)
    count=models.IntegerField(("count"),default=0)



class badges(models.Model):
    id=models.IntegerField(("id"),primary_key=True)
    # user_id=models.IntegerField(null=False)
    user_id = models.ForeignKey(users,on_delete = models.CASCADE)
    Class=models.SmallIntegerField(null=False)
    name=models.CharField(("name"),max_length=64,null=False)
    tag_based=models.BooleanField(("tag_based"),null=False)
    date= models.DateTimeField(("date"),auto_now_add=True,null=False)



class votes(models.Model):
    id=models.IntegerField(("id"),primary_key=True)
    # user_id=models.IntegerField(("user_id"),null=True)
    user_id = models.ForeignKey(users,related_name = 'user_id',on_delete = models.CASCADE)
    # post_id=models.IntegerField(("post_id"), null=False)
    post_id = models.ForeignKey(posts,related_name = 'post_id_votes',on_delete = models.CASCADE)
    vote_type_id=models.SmallIntegerField(("vote_type_id"), null=False)
    bounty_amount=models.SmallIntegerField(("bounty_amount"),null=True)
    creation_date=models.DateTimeField(("creation_date"), auto_now_add=True,null=False)


class comments(models.Model):
    id=models.IntegerField(("id"),primary_key=True)
    # post_id=models.IntegerField(("post_id"), null=False)
    post_id = models.ForeignKey(posts,on_delete = models.CASCADE) 
    # user_id=models.IntegerField(("user_id"),null=True)
    user_id = models.ForeignKey(users,on_delete = models.SET('Anonymous'))
    score=models.SmallIntegerField(("score"), null=False)
    content_license=models.CharField(("content_license"),max_length=64,null=False)
    user_display_name=models.CharField(("user_display_name",),max_length=64,null=True)
    text=models.TextField(("text"),null=True)
    creation_date=models.DateTimeField(("creation_date"),auto_now_add=True,null=False)



class post_history(models.Model):
    id=models.IntegerField(("id"),primary_key=True)
    # post_id=models.IntegerField(("post_id"), null=False)
    post_id = models.ForeignKey(posts,on_delete = models.CASCADE)
    # user_id=models.IntegerField(("user_id"), null=True)
    user_id = models.ForeignKey(users,on_delete = models.SET('Anonymous'))
    post_history_type_id=models.SmallIntegerField(("post_history_type_id"), null=False)
    user_display_name=models.CharField(("user_display_name"),max_length=64,null=True)
    content_license=models.CharField(("content_license"),max_length=64, null=True)
    revision_guid=models.UUIDField(("revision_guid"))
    text=models.TextField(("text"), null=True)
    comment=models.TextField(("comment"),null=True)
    creation_date=models.DateTimeField(("creation_date"),auto_now_add=True,null=False)


class post_links(models.Model):
    id=models.IntegerField(("id"),primary_key=True)
    # related_post_id=models.IntegerField(("related_post_id"), null=False)
    related_post_id = models.ForeignKey(posts,related_name = 'related_post_id',on_delete = models.PROTECT)
    # post_id=models.IntegerField(("post_id"), null=False)
    post_id = models.ForeignKey(posts,related_name = 'post_id_links',on_delete = models.CASCADE)
    link_type_id=models.SmallIntegerField(("link_type_id"), null=False)
    creation_date=models.DateTimeField(("creation_date"),auto_now_add=True,null=False)



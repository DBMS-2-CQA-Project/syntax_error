from django.db import models


# -- Tags
# CREATE TABLE tags (
# 	id SERIAL PRIMARY KEY,
# 	excerpt_post_id INTEGER,
# 	wiki_post_id INTEGER,
# 	tag_name VARCHAR(255) NOT NULL,
# 	count INTEGER DEFAULT 0
# );

# Create your models here.

class tags(models.Model):
    id=models.IntegerField(("id"),primary_key=True)
    excerpt_post_id=models.IntegerField(("excerpt_post_id"),null=True)
    wiki_post_id=models.IntegerField(("wiki_post_id"),null=True)
    tag_name=models.CharField(("tag_name"),max_length=255,null=False)
    count=models.IntegerField(("count"),default=0)



class badges(models.Model):
    id=models.IntegerField(("id"),primary_key=True)
    user_id=models.IntegerField(null=False)
    Class=models.SmallIntegerField(null=False)
    name=models.CharField(("name"),max_length=64,null=False)
    tag_based=models.BooleanField(("tag_based"),null=False)
    date= models.DateTimeField(("date"),auto_now_add=True,null=False)



class votes(models.Model):
    id=models.IntegerField(("id"),primary_key=True)
    user_id=models.IntegerField(("user_id"),null=True)
    post_id=models.IntegerField(("post_id"), null=False)
    vote_type_id=models.SmallIntegerField(("vote_type_id"), null=False)
    bounty_amount=models.SmallIntegerField(("bounty_amount"),null=True)
    creation_date=models.DateTimeField(("creation_date"), auto_now_add=True,null=False)


class comments(models.Model):
    id=models.IntegerField(("id"),primary_key=True)
    post_id=models.IntegerField(("post_id"), null=False)
    user_id=models.IntegerField(("user_id"),null=True)
    score=models.SmallIntegerField(("score"), null=False)
    content_license=models.CharField(("content_license"),max_length=64,null=False)
    user_display_name=models.CharField(("user_display_name",),max_length=64,null=True)
    text=models.TextField(("text"),null=True)
    creation_date=models.DateTimeField(("creation_date"),auto_now_add=True,null=False)



class post_history(models.Model):
    id=models.IntegerField(("id"),primary_key=True)
    post_id=models.IntegerField(("post_id"), null=False)
    user_id=models.IntegerField(("user_id"))
    post_history_type_id=models.SmallIntegerField(("post_history_type_id"), null=False)
    user_display_name=models.CharField(("user_display_name"),max_length=64)
    content_license=models.CharField(("content_license"),max_length=64)
    revision_guid=models.UUIDField(("revision_guid")),
    text=models.TextField(("text"))
    comment=models.TextField(("comment"))
    creation_date=models.DateTimeField(("creation_date"),auto_now_add=True,null=False)


    # id SERIAL PRIMARY KEY,
    # related_post_id INTEGER NOT NULL,
    # post_id INTEGER NOT NULL,
    # link_type_id SMALLINT NOT NULL,
    # creation_date TIMESTAMP NOT NULL

class post_links(models.Model):
    id=models.IntegerField(("id"),primary_key=True)
    related_post_id=models.IntegerField(("related_post_id"), null=False)
    post_id=models.IntegerField(("post_id"), null=False)
    link_type_id=models.SmallIntegerField(("link_type_id"), null=False)
    creation_date=models.DateTimeField(("creation_date"),auto_now_add=True,null=False)


class posts(models.Model):
    id=models.IntegerField(("id"),primary_key=True)
    owner_user_id=models.IntegerField(("owner_user_id"))
    last_editor_user_id=models.IntegerField(("last_editor_user_id"))
    post_type_id=models.SmallIntegerField(("post_type_id"), null=False)
    accepted_answer_id=models.IntegerField(("accepted_answer_id"))
    score=models.IntegerField(("score"), null=False)
    parent_id=models.IntegerField(("parent_id"))
    view_count=models.IntegerField(("view_count"))
    answer_count=models.IntegerField(("answer_count"), default = 0)
    comment_count=models.IntegerField(("comment_count"), default = 0)
    owner_display_name=models.CharField(("owner_display_name"),max_length=64)
    last_editor_display_name=models.CharField(("last_editor_display_name"),max_length=64)
    title=models.CharField(("title"),max_length=512)
    tags=models.CharField(("tags"),max_length=512),
    content_license=models.CharField(("content_license"),max_length=64, null=False)
    body=models.TextField(("body"))
    favorite_count=models.IntegerField(("favorite_count"))
    creation_date=models.DateTimeField(("creation_date"),auto_now_add=True,null=False)
    community_owned_date=models.DateTimeField(("community_owned_date"),auto_now_add=True)
    closed_date=models.DateTimeField(("closed_date"),auto_now_add=True)
    last_edit_date=models.DateTimeField(("last_edit_date"),auto_now_add=True)
    last_activity_date=models.DateTimeField(("last_activity_date"),auto_now_add=True)




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

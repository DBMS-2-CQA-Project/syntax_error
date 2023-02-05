from django.db import models

# # Create your models here.

# class tags(models.Model):
#     id=models.IntegerField(("id"),primary_key=True)
#     excerpt_post_id=models.IntegerField(("excerpt_post_id"))
#     tag_name=models.CharField(("tag_name"),max_length=255,null=False)
#     wiki_post_id=models.IntegerField(("wiki_post_id"))
#     count=models.IntegerField(("count"),default=0)

# class users(models.Model):
#     id=models.IntegerField(("id"),primary_key=True)
#     account_id=models.IntegerField(("account_id"),null=True)
#     reputation=models.IntegerField(("reputation"),null=False)
#     views=models.IntegerField(("views"),null=True)
#     down_votes=models.IntegerField(("down_votes"),default=0,null=True)
#     up_votes=models.IntegerField(("up_votes"),default=0,null=True)
#     display_name=models.CharField(("display_name"),max_length=255,null=False)
#     location=models.CharField(("location"),max_length=512,null=True)
#     profile_image_url=models.CharField(("profile_image_url"),max_length=255,null=True)
#     website_url=models.CharField(("website_url"),max_length=255,null=True)
#     about_me=models.TextField(("about_me"),null=True)

# class users(models.Model):
#     id=models.IntegerField(("id"),primary_key=True)
#     account_id=models.IntegerField(("account_id"),null=True)
#     reputation=models.IntegerField(("reputation"),null=False)
#     views=models.IntegerField(("views"),null=True)
#     down_votes=models.IntegerField(("down_votes"),default=0,null=True)
#     up_votes=models.IntegerField(("up_votes"),default=0,null=True)
#     display_name=models.CharField(("display_name"),max_length=255,null=False)
#     location=models.CharField(("location"),max_length=512,null=True)
#     profile_image_url=models.CharField(("profile_image_url"),max_length=255,null=True)
#     website_url=models.CharField(("website_url"),max_length=255,null=True)
#     about_me=models.TextField(("about_me"),null=True)

class user(models.Model):
    id=models.IntegerField(("id"),primary_key=True)
    account_id=models.IntegerField(("account_id"))
    reputation=models.IntegerField(("reputation"),null=False)
    views=models.IntegerField(("views"),null=True)
    down_votes=models.IntegerField(("down_votes"),default=0,null=True)
    up_votes=models.IntegerField(("up_votes"),default=0,null=True)
    display_name=models.CharField(("display_name"),max_length=255,null=False)
    location=models.CharField(("location"),max_length=512,null=True)
    about_me=models.TextField(("about_me"),null=True)

# class tags(models.Model):
#     id=models.IntegerField(("id"),primary_key=True)
#     excerpt_post_id=models.IntegerField(("excerpt_post_id"))
#     wiki_post_id=models.IntegerField(("wiki_post_id"))
#     tag_name=models.CharField(("tag_name"),max_length=255,null=False)
#     count=models.IntegerField(("count"),default=0)


# class posts(models.Model):
#     id=models.IntegerField(("id"),primary_key=True)
#     owner_user_id=models.IntegerField(("owner_user_id"))
#     tags=models.CharField(("tags"),max_length=512),
#     content_license=models.CharField(("content_license"),max_length=64, null=False)
#     body=models.TextField(("body"))
#     favorite_count=models.IntegerField(("favorite_count"))
#     creation_date=models.DateTimeField(("creation_date"),auto_now_add=True,null=False)
#     community_owned_date=models.DateTimeField(("community_owned_date"),auto_now_add=True)
#     closed_date=models.DateTimeField(("closed_date"),auto_now_add=True)
#     last_edit_date=models.DateTimeField(("last_edit_date"),auto_now_add=True)
#     last_activity_date=models.DateTimeField(("last_activity_date"),auto_now_add=True)




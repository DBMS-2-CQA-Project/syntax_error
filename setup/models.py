from django.db import models

# Create your models here.




# class tags(models.Model):
#     id=models.IntegerField(("id"),primary_key=True)
#     excerpt_post_id=models.IntegerField(("excerpt_post_id"))
#     tag_name=models.CharField(("tag_name"),max_length=255,null=False)
#     wiki_post_id=models.IntegerField(("wiki_post_id"))
#     count=models.IntegerField(("count"),default=0)

# class users(models.Model):
#     id=models.IntegerField(("id"),primary_key=True)
#     account_id=models.IntegerField(("account_id"))
#     reputation=models.IntegerField(("reputation"),null=False)
#     views=models.IntegerField(("views"))
#     down_votes=models.IntegerField(("down_votes"),default=0)
#     up_votes=models.IntegerField(("up_votes"),default=0)
#     display_name=models.CharField(("display_name"),max_length=255,null=False)
#     location=models.CharField(("location"),max_length=512)
#     profile_image_url=models.CharField(("profile_image_url"),max_length=255)
#     website_url=models.CharField(("website_url"),max_length=255)
#     about_me=models.TextField(("about_me"))
#     creation_date=models.TimeField(("creation_date"),null=False)
#     last_access_date=models.TimeField(("last_access_date"),null=False)


class users(models.Model):
    account_id=models.IntegerField(("account_id"))
    pw=models.CharField(("pw"),max_length=10,null=False)
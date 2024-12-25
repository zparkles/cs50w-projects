from django.contrib.auth.models import AbstractUser
from django.db import models

class CreatePost(models.Manager):
    def create_post(self, post, author):
        posting = self.create(post=post, author=author)
        return posting
    

class CreateLike(models.Manager):
    def create_like(self, status, post_liked, user):
        liking = self.create(status=status, post_liked=post_liked, user=user)
        return liking

class FollowAccount(models.Manager):
    def follow_acc(self, follow, account, user):
        following = self.create(follow=follow, account=account, user=user)
        return following




class User(AbstractUser):
    pass

class Post(models.Model) :
    post = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name="posts", default=0)
    date_posted = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)
    objects = CreatePost()
    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "post": self.post,
            "date_posted": self.date_posted.strftime("%b %d %Y, %I:%M %p"),
            "like_count": self.like_count
        }
    def __str__(self):
        return f'{self.author} : {self.post}'

class Like(models.Model) :
    status = models.BooleanField(default='')
    post_liked = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="like", default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="liked", default=0 )
    objects = CreateLike()
    def serialize(self):
        return {
            "id": self.id,
            "post_liked": self.post_liked.id, #liked post
            "status": self.status,
            "user": self.user.id, #the user following/ not following that account
        }
    def __str__(self):
         if self.status == True:
            return f'{self.user} liked {self.post_liked.post}'
         else: 
             return f'{self.user} unliked {self.post_liked.post}'

class Follow(models.Model):
    follow = models.BooleanField()
    account = models.ForeignKey(User,on_delete=models.CASCADE, related_name="following", default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="follower", default=0)
    objects = FollowAccount()
    def serialize(self):
        return {
            "id": self.id,
            "follow": self.follow,
            "account": self.account.id, #account thats being followed
            "user": self.user.id, #the user following/ not following that account
        }
    def __str__(self):
        if self.follow == True:
            return f'{self.user} followed {self.account}'
        else:
            return f'{self.user} unfollowed {self.account}'
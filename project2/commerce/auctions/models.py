from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class CreateListing(models.Manager):
    def create_listing(self, title, description, starting_bid, image, category, author):
        listing = self.create(title=title, description=description, starting_bid=starting_bid,
                           image=image, category=category, author=author)
        return listing
    

class CreateBid(models.Manager):
    def create_bid(self, bid, bidder, bid_object):
        bidding = self.create(bid=bid, bidder=bidder, bid_object=bid_object)
        return bidding

class CreateComment(models.Manager):
    def create_comment(self, comment, account, comment_object):
        commenting = self.create(comment=comment, account=account, comment_object=comment_object)
        return commenting

class Listings(models.Model):
    category_list = [
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics'),
        ('Home', 'Home'),
        ('Others', 'Others')
    ]
    title = models.CharField(max_length=50)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=12, decimal_places=0)
    image = models.ImageField(null= True, blank=True, upload_to='auctions/images/')
    category = models.CharField(choices=category_list, blank=True, max_length=15)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name="posts", default=0)
    status= models.BooleanField(default=True)
    objects = CreateListing()
    def __str__(self):
        return self.title


class Bid(models.Model):
    bid = models.DecimalField(max_digits=12, decimal_places=0)
    bidder = models.ForeignKey(User,on_delete=models.CASCADE, related_name="bid_value", default=0)
    bid_object= models.ForeignKey(Listings,on_delete=models.CASCADE, related_name="bid", default=0)
    objects = CreateBid()
    def __str__(self):
        return f"{self.bidder}: {self.bid} on {self.bid_object}"

class Comment(models.Model):
    comment = models.CharField(max_length=500)
    account = models.ForeignKey(User,on_delete=models.CASCADE, related_name="comments", default=0)
    comment_object= models.ForeignKey(Listings,on_delete=models.CASCADE, related_name="commented", default=0)
    objects = CreateComment()
    def __str__(self):
        return f"{self.account} : {self.comment} on {self.comment_object}"  
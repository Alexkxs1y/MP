from django.contrib.auth.models import AbstractUser
from django.db import models

#for timestamp
from django.utils.timezone import now

#for resizing
from PIL import Image


class User(AbstractUser):
    pass

class Category(models.Model): 
    category = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.category}"

class Auction_listing(models.Model):
    listing_title = models.CharField(max_length=64)
    listing_description = models.TextField(verbose_name="Description", default=None, blank=True)
    # category_id = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="category_reverse")
    category = models.ManyToManyField(Category, blank=True, related_name="category_reverse")
    starting_bid = models.IntegerField()
    current_price = models.IntegerField(blank=True)    
    picture = models.ImageField(blank=True, upload_to='images', default='images/No_Image_Available.jpg')
    actual = models.IntegerField(default=1)
    winnerid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner_reverse", default=None, blank=True)
    ownerid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_reverse", default=None, blank=True)
    # created = models.DateTimeField(auto_now_add=True, blank=True)
    created = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return f"{self.id} == {self.listing_title}"

    def save(self):
        super().save()
        img = Image.open(self.picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.picture.path)    

class Bids(models.Model):
    listingid = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="listing_reverse2")
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reverse2")
    bid = models.IntegerField(verbose_name="")
    created = models.DateTimeField(default=now, editable=False)  

    def __str__(self):
        return f"{self.bid}"

""" class Categories(models.Model): 
    listing_id = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="listing_reverse5")    
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_reverse5")          """

class Comments(models.Model):
    listingid = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="listing_reverse3")
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reverse3")
    comment = models.TextField(verbose_name="")
    created = models.DateTimeField(default=now, editable=False) 

    def __str__(self):
        return f"{self.comment}"

class Whatchlist(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reverse4")
    #userid = models.ManyToManyField(User)
    listingid = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="listing_reverse4")
    #on_watchlist = models.IntegerField(default=0)
    #inwatchlist = models.BooleanField(verbose_name="Watchlist", default=False)
    created = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        # return f"{self.userid, self.listingid}"
        return f"{self.id} == {self.userid} - {self.listingid}"

    
              

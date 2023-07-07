from django.contrib import admin

# Register your models here.
from .models import  Category, Auction_listing, Bids, Comments, Whatchlist

admin.site.register(Category)
admin.site.register(Auction_listing)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Whatchlist)

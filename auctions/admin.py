from django.contrib import admin

from .models import AuctionListings, User, Categories, Bids, Comments

admin.site.register(AuctionListings)
admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Bids)
admin.site.register(Comments)

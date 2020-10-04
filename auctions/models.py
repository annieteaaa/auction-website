from django.contrib.auth.models import AbstractUser
from django.db import models

#remember to make migrations and migrate for changes

class User(AbstractUser):
    pass

class Categories(models.Model):
    category = models.CharField(max_length=64)

class AuctionListings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    title = models.CharField(max_length=64)
    photo = models.URLField(blank=True)
    description = models.CharField(max_length=300)
    starting = models.DecimalField(max_digits=6, decimal_places=2)
    watcher = models.ManyToManyField(User, null=True, related_name="watchlist")
    running = models.BooleanField(default=True)
    winner = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, related_name="wins")
    category = models.ForeignKey(Categories, default=5, on_delete=models.PROTECT, related_name="listings")
    current = models.DecimalField(max_digits=6, decimal_places=2, null=True)

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    item = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="bids")

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=300)
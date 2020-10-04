from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, AuctionListings, Bids, Comments, Categories
from django.db.models import Max
from django.contrib.auth.decorators import login_required

def index(request):
    listings = AuctionListings.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html")
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting = request.POST["starting"]
        photo = request.POST["photo"]
        category = request.POST["category"]
        listing = AuctionListings(user=request.user, title=title, photo=photo, description=description, starting=starting, category_id=category)
        listing.save()
        return HttpResponseRedirect(reverse("item", args=(listing.id,)))
    return render(request, "create/create.html", {
        "categories": Categories.objects.all()
    })

def item(request, listnum):
    listing = AuctionListings.objects.get(pk=listnum)
    current = listing.bids.all().aggregate(Max('amount'))['amount__max']
    if request.user in listing.watcher.all():
        return render(request, "auctions/item.html", {
            "listing": listing,
            "message": "Remove from Watchlist",
            "active": listing.running,
            "comments": listing.comments.all(),
            "poster": request.user == listing.user,
        })
    else:
        return render(request, "auctions/item.html", {
            "listing": listing,
            "active": listing.running,
            "comments": listing.comments.all(),
            "poster": request.user == listing.user,
        })

@login_required
def watch(request, listnum):
    listing = AuctionListings.objects.get(pk=listnum)
    listing.watcher.add(request.user)
    return item(request, listnum)

@login_required
def unwatch(request, listnum):
    listing = AuctionListings.objects.get(pk=listnum)
    listing.watcher.remove(request.user)
    return item(request, listnum)

@login_required
def bid(request, listnum):
    if request.method == "POST":
        amount = float(request.POST["bidding"])
        listing = AuctionListings.objects.get(pk=listnum)
        if amount >= listing.starting:
            maxbid = listing.bids.all().aggregate(Max('amount'))['amount__max']
            if maxbid == None:
                newbid = Bids(user=request.user, amount=amount, item=listing)
                newbid.save()
                listing.current = '{:.2f}'.format(newbid.amount)
                listing.save()
                return render(request, "auctions/item.html", {
                    "listing": listing,
                    "message_success": "Bid Successful!",
                    "active": listing.running,
                    "comments": listing.comments.all(),
                    "winner": request.user == listing.bids.all().order_by('-amount').first().user,
                    "poster": request.user == listing.user,
                })
            elif amount > maxbid:
                newbid = Bids(user=request.user, amount=amount, item=listing)
                newbid.save()
                listing.current = '{:.2f}'.format(newbid.amount)
                listing.save()
                return render(request, "auctions/item.html", {
                    "listing": listing,
                    "message_success": "Bid Successful!",
                    "active": listing.running,
                    "comments": listing.comments.all(),
                    "poster": request.user == listing.user,
                })
            else:
                return render(request, "auctions/item.html", {
                    "listing": listing,
                    "poster": request.user == listing.user,
                    "active": listing.running,
                    "comments": listing.comments.all(),
                    "message_fail2": "Please bid higher than the current bid."
                })
        else:
            return render(request, "auctions/item.html", {
                "listing": listing,
                "poster": request.user == listing.user,
                "active": listing.running,
                "comments": listing.comments.all(),
                "message_fail1": "Please bid at least the starting amount."
            })
    return item(request, listnum)

@login_required
def close(request, listnum):
    listing = AuctionListings.objects.get(pk=listnum)
    if request.user == listing.user:
        highest = listing.bids.all().order_by('-amount').first()
        listing.running = False
        listing.winner = highest.user
        listing.save()
        return render(request, "auctions/item.html", {
            "listing": listing,
            "poster": request.user == listing.user,
            "active": listing.running,
            "comments": listing.comments.all(),
        })
    else:
        return render(request, "auctions/item.html", {
            "listing": listing,
            "poster": request.user == listing.user,
            "active": listing.running,
            "comments": listing.comments.all(),
            "message_fail": "You are not authorized to close this auction."
        })

@login_required
def comment(request, listnum):
    if request.method == "POST":
        comment = request.POST["comment"]
        newcomment = Comments(user=request.user, item=AuctionListings.objects.get(pk=listnum), comment=comment)
        newcomment.save()
    return item(request, listnum)

@login_required
def listings(request):
    return render(request, "auctions/listings.html", {
        "listings": request.user.auctions.all()
    })

@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "listings": request.user.watchlist.all()
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Categories.objects.all()
    })

def category(request, listnum):
    category = Categories.objects.get(pk=listnum)
    return render(request, "auctions/category.html", {
        "category": category.category,
        "listings": category.listings.all()
    })
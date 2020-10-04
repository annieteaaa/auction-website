from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("item/<int:listnum>", views.item, name="item"),
    path("listings", views.listings, name="listings"),
    path("watch/<int:listnum>", views.watch, name="watch"),
    path("unwatch/<int:listnum>", views.unwatch, name="unwatch"),
    path("bid/<int:listnum>", views.bid, name="bid"),
    path("close/<int:listnum>", views.close, name="close"),
    path("comment/<int:listnum>", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<int:listnum>", views.category, name="category"),
]
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="contactus"),
    path("tracker/", views.tracker, name="trakingStatus"),
    path("search/", views.search, name="search"),
    path("products/<int:id>", views.products, name="products"),
    path("checkout/", views.checkout, name="Checkout"),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
]

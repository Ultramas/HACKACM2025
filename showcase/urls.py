from django.urls import path
from . import views

app_name = 'showcase'
urlpatterns = [
    path("analyze/", views.analyze, name="analyze"),
    path("", views.index, name="index"),
    path("api_listings", views.index, name="api_listings"),
]


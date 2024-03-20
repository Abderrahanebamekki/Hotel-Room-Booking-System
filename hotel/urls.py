from django.urls import path,include

from hotel.views import Search

urlpatterns = [
    path('search/', Search.as_view(), name='search')
]
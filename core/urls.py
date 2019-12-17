from django.conf.urls import url
from .views import home_view

urlpatterns = [
    url('', home_view, name="home_view"),
]
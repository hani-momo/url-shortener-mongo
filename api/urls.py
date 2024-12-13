from django.urls import path, re_path
from .views import ShortenURLView, RedirectView


urlpatterns = [
    path('shorten/', ShortenURLView.as_view(), name='shorten_url'),
    re_path(r'^redirect/(?P<short_url>.*)/$', RedirectView.as_view(), name='redirect_url'),
]

from django.contrib import admin
from django.urls import path
from api.views import ShortenURLView, RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('shorten/', ShortenURLView.as_view(), name='shorten_url'),
    path('r/<str:short_url>/', RedirectView.as_view(), name='redirect_url'),
]

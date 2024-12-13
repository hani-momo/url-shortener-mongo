from django.urls import include, path


urlpatterns = [
    path('api/', include(('api.urls', 'api'), namespace='api')),
]

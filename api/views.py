import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mongoengine import DoesNotExist
from .models import URL
from .utils import create_short_url
from .utils import ShortURLAlreadyExists


logger = logging.getLogger(__name__)

class ShortenURLView(APIView):
    def post(self, request):
        '''Expects a JSON body with 'url' field'''
        original_url = request.data.get('url')
        if not original_url:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            short_url = create_short_url(original_url)
            return Response({"shortened_url": short_url}, status=status.HTTP_201_CREATED)
        except ShortURLAlreadyExists:
            return Response({"error": "Short URL already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error shortening original URL: {e}")
            return Response({"error": "An error while shortening the URL"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RedirectView(APIView):
    def get(self, request, short_url):
        '''Expects short URL as a path param.'''
        if not short_url or len(short_url) != 6:
            return Response({"error": "Invalid Short URL."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            url_entry = URL.objects.get(shortened_url=short_url)
            return Response({"original_url": url_entry.original_url}, status=status.HTTP_200_OK)
        except DoesNotExist:
            return Response({"error": "Short URL not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving original URL: {e}")
            return Response({"error": "An error occurred while retrieving the original URL"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
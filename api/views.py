import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mongoengine import DoesNotExist
from .models import URL
from .services import generate_short_url


logger = logging.getLogger(__name__)

class ShortenURLView(APIView):
    def post(self, request):
        try:
            original_url = request.data.get('url')
            if not original_url:
                logger.warning("No URL provided.")
                return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

            short_url = generate_short_url(original_url=original_url)
            url_entry = URL(original_url=original_url, shortened_url=short_url)
            url_entry.save()

            return Response({"shortened_url": short_url}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error shortening URL: {e}")
            return Response({"error": "An error while shortening the URL"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RedirectView(APIView):
    def get(self, request, short_url):
        try:
            logger.info(f"Short URL: {short_url}")
            url_entry = URL.objects.get(shortened_url=short_url)
            return Response({"original_url": url_entry.original_url}, status=status.HTTP_200_OK)
        except DoesNotExist:
            logger.error(f"Short URL not found: {short_url}")
            return Response({"error": "Short URL not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving original URL: {e}")
            return Response({"error": "An error occurred while retrieving the original URL"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mongoengine import DoesNotExist
from .models import URL
from .services import generate_short_url


logger = logging.getLogger(__name__)

<<<<<<< HEAD
=======
def generate_short_url(length: int = 6) -> str:
    """
    Generate a random short URL string.

    Args:
        length: The length of the generated short URL. By default is 6.

    Returns:
        str: A randomly generated short URL of letters and digits.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

>>>>>>> origin/master
class ShortenURLView(APIView):
    def post(self, request) -> Response:
        """
        Args:
            request: object with the URL to shorten.

        Returns:
            Response: object with the shortened URL or an error message.
        """
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
    def get(self, request, short_url) -> Response:
        """
        Handle GET requests, retrieve the original URL from a shortened URL.

        Args:
            request
            short_url (str)

        Returns:
            Response: object with the original URL or an error message.
        """
        try:
            logger.info(f"Short URL: {short_url}")
            url_entry = URL.objects.get(shortened_url=short_url)
            return Response({"original_url": url_entry.original_url}, status=status.HTTP_200_OK)
        except DoesNotExist:
            logger.error(f"Short URL not found: {short_url}")
            return Response({"error": "Short URL not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving original URL: {e}")
<<<<<<< HEAD
            return Response({"error": "An error occurred while retrieving the original URL"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
=======
            return Response({"error": "An error occurred while retrieving the original URL"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
            # return HttpResponseRedirect(url_entry.original_url)
>>>>>>> origin/master

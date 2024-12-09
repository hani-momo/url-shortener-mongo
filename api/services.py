import base64
import os
import logging
from .models import URL


logger = logging.getLogger(__name__)

def generate_short_url(original_url, length=6):
    existing_entry = get_existing_entry(original_url)
    if existing_entry:
        logger.info(f"This URL already exists in db: {original_url}. Returning existing short URL for it: {existing_entry.shortened_url}")
        return f"URL already exists in db. The short URL for it: {existing_entry.shortened_url}"

    while True:
        random_bytes = os.urandom(length)
        short_url = base64.urlsafe_b64encode(random_bytes).decode('utf-8')[:length]

        if short_url_exists(short_url):
            logger.warning(f"Generated an existing short URL. Another try...")
            continue
        else:
            save_url_mapping(original_url, short_url)
            logger.info(f"Generated a new short URL: {short_url} for original URL: {original_url}")
            return short_url

def get_existing_entry(original_url):
        entries = URL.objects.filter(original_url=original_url)
        if entries.count() > 1:
            logger.warning(f"Multiple entries found for original URL: {original_url}. Returning the first one.")            
        return entries.first()

def short_url_exists(short_url):
    try:
        URL.objects.get(shortened_url=short_url)
        return True
    except URL.DoesNotExist:
        return False
    except Exception as e:
        logger.error(f"Error checking if short URL exists: {e}")
        return False

def save_url_mapping(original_url, short_url):
    URL.objects.create(original_url=original_url, shortened_url=short_url)
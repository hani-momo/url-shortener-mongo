import base64
import logging
import random
from typing import Optional

from .models import URL


logger = logging.getLogger(__name__)

class ShortURLAlreadyExists(Exception):
    '''Custom Exception to handle case when short URL already exists'''
    pass


def generate_unique_short_url(original_url: str, length: int = 6) -> str:
    """utils code
    Generates a unique short URL based on the original URL.
    If the generated short URL already exists, it will generate a new one.
    
    Args:
        original_url (str): The original URL to shorten.
        length (int): The length of the short URL.
    
    Returns:
        str: A unique shortened URL.
    """
    original_url_bytes = original_url.encode("ascii")
    base64_bytes = base64.b64encode(original_url_bytes)
    base64_string = base64_bytes.decode("ascii")

    max_attempts = 10
    attempts = 0

    while attempts < max_attempts:
        start_index = random.randint(0, len(base64_string) - length)
        shortened = base64_string[start_index:start_index + length]

        if not URL.objects.filter(shortened_url=shortened).first():
            return shortened
        
        attempts += 1

    raise ShortURLAlreadyExists("Unable to generate a unique short URL after multiple attempts.")


def check_existing_entry(original_url: str) -> Optional[URL]:
    '''
    Check if an entry original url already exists in the database.

    Args: 
        original_url (str): The URL to check.

    Returns:
        The original URL if exists, otherwise None
    '''
    try:
        entry = URL.objects.filter(original_url=original_url).first()
        return entry
    except Exception as e:
        logger.exception(f"Error checking existing entry: {e}")
        return None


def create_url_mapping(original_url: str, short_url: str):
    '''Creates a URL mapping in the database if it does not already exist.'''
    try:
        if not URL.objects.filter(original_url=original_url).first():
            URL.objects.create(original_url=original_url, shortened_url=short_url)
        else:
            logger.warning(f"URL already exists.")
    except Exception as e:
        logger.exception(f"Error creating short URL: {e}")
        raise


def create_short_url(original_url: str, length: int=6) -> str:
    '''
    If the original url already exists in the database, returns the existing short url.
    Otherwise, generates a new short url.

    Args:
        original_url (str): The original URL to shorten.
        length (int): The length of the short url

    Returns:
        str: The generated short URL.
    '''
    try:
        existing_entry = check_existing_entry(original_url)
        if existing_entry:
            return existing_entry.shortened_url

        shortened = generate_unique_short_url(original_url, length)
        create_url_mapping(original_url, shortened)
        return shortened

    except Exception as e:
        logger.exception(f"Error creating short URL: {e}")
        raise
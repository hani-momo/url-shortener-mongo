import base64
import os
import logging
from .models import URL
from typing import Optional
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)

class ShortURLAlreadyExists(Exception):
    '''Custom Exception to handle case when short URL already exists'''
    pass

def generate_short_url(length: int=6) -> str:
    '''
    Generate a short url for the original with base64 encoding.

    Args:
        length (int): The length of the short url

    Returns:
        str: The generated short URL.
    '''
    random_bytes = os.urandom(length)
    short_url = base64.urlsafe_b64encode(random_bytes).decode('utf-8')[:length]
    return short_url

def create_short_url(original_url: str) -> str:
    '''
    Create a unique short URL for the original within 5 attempts.
    If the original url already exists in the database, returns the existing short url.

    Args:
        original_url (str): The original URL to shorten.

    Returns:
        str: The generated or already existing short URL.
    '''
    existing_entry = check_existing_entry(original_url)
    if existing_entry:
        return existing_entry.shortened_url
    
    count_attempt = 5
    while count_attempt > 0:
        short_url = generate_short_url()
        count_attempt -= 1

        if not is_short_url_exist(short_url):
            save_url_mapping(original_url, short_url)
            return short_url
    raise ShortURLAlreadyExists

def check_existing_entry(original_url: str) -> Optional[URL]:
    '''
    Check if an entry original url already exists in the database.

    Args: 
        original_url (str): The URL to check.

    Returns:
        The original URL if exists, otherwise None
    '''
    entry = URL.objects.filter(original_url=original_url).first()
    if entry:
        return entry
    return None

def is_short_url_exist(short_url: str) -> bool:
    '''
    Checks if short URL already exists in the databse.

    Args:
        short_url (str): Short URL to check.

    Returns:
        bool: True if short URL exists, otherwise False.
    '''
    try:
        if URL.objects.filter(shortened_url=short_url).exists():
            return True
    except URL.DoesNotExist:
        return False
    except Exception as e:
        logger.error(f"Error checking if short URL exists: {e}")
        return False

def save_url_mapping(original_url: str, short_url: str) -> None:
    '''
    Saves the mapping of the original URL to the short URL in the databse.

    Args:
        original_url (str): The original URL to save.
        short_url (str): The generated short URL to save.
    Returns:
        None
    '''
    URL.objects.create(original_url=original_url, shortened_url=short_url)
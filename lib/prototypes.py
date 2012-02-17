"""Section and Index prototypes are here for easy access and default values.
xxxIndex and xxxSection classes should inherit from those
"""
import urlparse
import urllib
import re


class Index(object):
    """Parent class for all Index classes.
    """
    
    
    title = str
    author = str
    sections = list()
    images = list()
    dirname = str
    dirname_no_slash = str
    

class Section(object):
    """Parent class for all section classes.
    """
    
    
    title = str
    url = str
    content = list()
    filename = str
    dirname = str

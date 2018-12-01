# Main Request Handler
# Include pages
# / and /index
# also /search page
# and others pages

import tornado.web
import logging
from BaseHandler import *


class HomeHandler(BaseHandler):
    """
        The Home page handler.
    """
    pass

class SearchHandler(BaseHandler):
    """
        The search page handler.
    """
    pass

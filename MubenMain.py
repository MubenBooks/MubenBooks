# Main Request Handler
# Include pages
# / and /index
# also /search page
# and others pages

import tornado.web

import logging


class HomeHandler(tornado.web.RequestHandler):
    """
        The Home page handler.
    """
    pass

class SearchHandler(tornado.web.RequestHandler):
    """
        The search page handler.
    """
    pass

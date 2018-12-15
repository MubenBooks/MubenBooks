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
    @tornado.web.authenticated
    async def get():
    	user = self.get_secure_cookie('muben_user')
    	self.write(user)

class SearchHandler(BaseHandler):
    """
        The search page handler.
    """
    pass

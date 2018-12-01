# The Auth Reuqest module
# login 
# logout
# register
import logging
import tornado.web
from BaseHandler import *

class AuthLoginHandler(BaseHandler):
    """
        Login Request handler
    """
    def get(self):
        self.write("I am login module")


class AuthLogoutHandler(BaseHandler):
    """
        Logout Request Handler
    """
    def get(self):
        self.write("I am logout module")


class AuthRegisterHandler(BaseHandler):

    """
        Register request handler
    """
    def get(self):
        self.write("I am register module!")

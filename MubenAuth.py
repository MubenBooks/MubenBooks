# The Auth Reuqest module
# login 
# logout
# register
import logging
import tornado.web


class AuthLoginHandler(tornado.web.RequestHandler):
    """
        Login Request handler
    """
    def get(self):
        self.write("I am login module")


class AuthLogoutHandler(tornado.web.RequestHandler):
    """
        Logout Request Handler
    """
    def get(self):
        self.write("I am logout module")


class AuthRegisterHandler(tornado.web.RequestHandler):

    """
        Register request handler
    """
    def get(self):
        self.write("I am register module!")

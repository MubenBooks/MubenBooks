# Admin Request Handler
# Manager for adding books and configure database
# Later will support users manage
import logging
import tornado.web
from BaseHandler import BaseHandler


class IndexHandler(BaseHandler):
    """
        Admin page Index Request Handler
    """
    def get(self):
        self.write("Hello I am admin manager")


class BooksManagerHandler(BaseHandler):
    """
        The page off mange books

        Function:
        add -- add ebooks information and file path to database
        delete --delete ebook info from database
    """

    def get(self):
        self.write("Hello, here is book manager page")


class AuthLoginHandler(BaseHandler):
    """
        Admin login Request Handler

    """
    def get(self):
        self.write("Login manager")

class AuthLogoutHandler(BaseHandler):
    """
        Admin logout Request handler
    """
    def get(self):
        self.write("admin logout manager")


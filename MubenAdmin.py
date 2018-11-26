# Admin Request Handler
# Manager for adding books and configure database
# Later will support users manage
import logging

import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    """
        Admin page Index Request Handler
    """
    def get(self):
        self.write("Hello I am admin manager")


class BooksManagerHandler(tornado.web.RequestHandler):
    """
        The page off mange books

        Function:
        add -- add ebooks information and file path to database
        delete --delete ebook info from database
    """

    def get(self):
        self.write("Hello, here is book manager page")


class AuthLoginManagerHandler(tonado.web.RequestHandler):
    """
        Admin login Request Handler

    """
    def get(self):
        self.write("Login manager")

class AuthLogoutMangerHandler(tornado.web.RequestHandler):
    """
        Admin logout Request handler
    """
    def get(self):
        self.write("admin logout manager")


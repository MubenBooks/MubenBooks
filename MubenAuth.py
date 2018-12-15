# The Auth Reuqest module
# login 
# logout
# register
import bcrypt
import logging
import tornado.escape
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
        self.render("create_user.html")

    async def post(self):
        username = self.get_argument("username", '')
        password = self.get_argument("password", '')
        # post_email = self.get_argument("post_email", '')
        register_email = self.get_argument("register_email", '')
        phone_number = self.get_argument("phone_num", '')

        if await self.any_user_exists(username):
            raise tornado.web.HTTPError(400, "用户已经存在")
        hashed_password = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                bcrypt.hashpw,
                tornado.escape.utf8(password),
                bcrypt.gensalt(),
        )

        user = await self.queryone(
                "INSERT INTO users (username, password, register_email, phone_num) "
                "VALUES (%s, %s, %s, %s) RETURNING id",
                username,
                tornado.escape.to_unicode(hashed_password),
                register_email,
                phone_number,
                )
        self.set_secure_cookie('muben_user', str(user.id))
        self.redirect(self.get_argument("next", "/"))





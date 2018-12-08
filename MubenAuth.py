# The Auth Reuqest module
# login 
# logout
# register
# import bcrypt
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
        self.render("create_user.html")

    async def post(self):
        if await self.any_user_exists(self.get_argument("username")):
            raise tornado.web.HTTPError(400, "用户已经存在")
        hashed_password = await tornado.ioloop.IOLoop.current().run_in_executor(
                None,
                bcrypt.hashpw,
                tornado.escape.utf8(self.get_argument("password")),
                bcrypt.gensalt(),
        )

        user = await self.queryone(
                "INSERT INTO users (username, password, post_email, register_email, phone_num) "
                "VALUES (%s, %s, %s, %s, %s) RETURN id",
                self.get_argument("username"),
                tornado.escape.to_unicode(hashed_password),
                self.get_argument("post_email"),
                self.get_argument("register_email"),
                self.get_argument("phone_num"),
                )
        self.set_secure_cookie('muben_user', str(user.id))
        self.redirect(self.get_argument("next", "/"))





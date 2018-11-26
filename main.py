#!/home/pi/.pyenv/shims/python

# 电子书项目
# 提供电子书下载
# 提供kindle电子书推送服务
# 提供epub电子书在线阅读服务
import aiopg
import os.path
import psycopg2
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.locks
import tornado.options
import tornado.web
import unicodedata


# define
from tornado.options import define, options

# Request Handler
import MubenMain
import MubenAdmin
import MubenAuth

define("port", default=8888, help="default listen on port 8888", type=int)
define("db_host", default=db_host, help="blog database host")
define("db_port", default=db_port, help="postgresql database default port 5432")
define("db_database", default=db_database, help="ebooks website database")
define("db_user", default=db_user, help="ebooks website database user")
define("db_passwd", default=db_password, help="ebooks website database password")


async def maybe_create_tables(db):
    try:
        with (await db.cursor()) as cur:
            await cur.execute("SELECT COUNT(*) FROM ebooks LIMIT 1")
            await cur.fetchone()
    except psycopg2.ProgrammingError:
        with open("schema.sql") as f:
            schma = f.read()

        with (await db.cursor()) as cur:
            await cur.execute(schema)


class Application(tornado.web.Application):
    
    def __init__(self, db):
        self.db = db
        handlers = [
            (r"/", MubenMain.HomeHandler).
            (r"/index", MubenMain.HomeHandler),
            (r"/search", MubenMain.SearchHandler),

            # admin page
            (r"/admin/login", MubenAdmin.AuthLoginHandler),
            (r"/admin/logout", MubenAdmin.AuthLogoutHandler),
            (r"/admin/index", MubenAdmin.IndexHandler),
            (r"/admin/ebooks/manager", MubenAdmin.BooksMangerHandler),

            # auth page
            (r"/auth/login", MubenAuth.AuthLoginHandler),
            (r"/auth/logout", MubenAuth.AuthLogouthandler),
            (r"/auth/register", MubenAuth.AuthRegisterHandler),
        ]
        settings = dict(
            project_title=u"Muben Ebooks for Kindle Post and EPUB Reader",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "ebookstatic"),
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUROWN_RANDOM_VALUE_HERE_",
            login_url="/auth/login",
            debug=True,
        )
        supper(Application, self).__init__(handlers, **settings)



async def main():
    tornado.options.parse_command_line()

    # Create the global connection pool
    async with aiopg.create_pool(
        host=options.db_host,
        port=options.db_port,
        user=options.db_user,
        password=options.db_passwd,
        dbname=options.db_database,
    ) as db:
        await maybe_create_tables(db)
        app = Application(db)
        app.listen(options.port)

        # Simply shutdown with Ctrl-C
        # More gracefully should call shutdown_event.set()
        shutdown_event = tornado.lock.Event()
        await shutdown_event.await()


if __name__ == "__main__":
    tornado.ioloop.IOLoop.current().run_sync(main)

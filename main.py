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
from utils.define import *
# Request Handler
import MubenMain
import MubenAdmin
import MubenAuth
import MubenBook
import FileHandler

define("port", default=8888, help="default listen on port 8888", type=int)
define("db_host", default=db_host, help="blog database host")
define("db_port", default=db_port, help="postgresql database default port 5432")
define("db_database", default=db_database, help="ebooks website database")
define("db_user", default=db_user, help="ebooks website database user")
define("db_passwd", default=db_password, help="ebooks website database password")
define("book_root_path", default=os.path.join(os.path.dirname(__file__), 
    'ebooks'), help = "default book store path")


async def maybe_create_tables(db):
    try:
        with (await db.cursor()) as cur:
            await cur.execute("SELECT COUNT(*) FROM books LIMIT 1")
            await cur.fetchone()
    except psycopg2.ProgrammingError:
        with open("schema.sql") as f:
            schema = f.read()

        with (await db.cursor()) as cur:
            await cur.execute(schema)


class Application(tornado.web.Application):
    
    def __init__(self, db):
        self.db = db
        handlers = [
            (r"/", MubenMain.HomeHandler),
            (r"/index", MubenMain.HomeHandler),
            (r"/search", MubenMain.SearchHandler),

            # 图书详情及功能页
            (r"/book", MubenBook.BookDetailsHandler),
            (r"/book/send", MubenBook.BookSendHandler),

            # admin page
            (r"/admin/login", MubenAdmin.AuthLoginHandler),
            (r"/admin/logout", MubenAdmin.AuthLogoutHandler),
            (r"/admin/index", MubenAdmin.IndexHandler),
            (r"/admin/ebooks/manager", MubenAdmin.BooksManagerHandler),

            # auth page
            (r"/auth/login", MubenAuth.AuthLoginHandler),
            (r"/auth/logout", MubenAuth.AuthLogoutHandler),
            (r"/auth/register", MubenAuth.AuthRegisterHandler),

            # File upload and get
            (r"/file/upload", FileHandler.UploadBookHandler),
            (r"/file/email", FileHandler.SendBookHandler),
            (r"/file/test_upload", FileHandler.TestHadnler),
        ]
        settings = dict(
            project_title=u"Muben Ebooks for Kindle Post and EPUB Reader",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "ebookstatic"),
            xsrf_cookies=True,
            cookie_secret="2hcicVu+TqShDpfsjMWQLZ0Mkq5NPEWSk9fi0zsSt3A=",
            login_url="/auth/login",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)



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
        shutdown_event = tornado.locks.Event()
        await shutdown_event.wait()


if __name__ == "__main__":
    tornado.ioloop.IOLoop.current().run_sync(main)


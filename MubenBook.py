# 图书详情页面
# 图书推送功能
import requests
from BaseHandler import *
import logging
from utils.smtp import *

UPLOAD_HOST = "http://file.aaron.mobi"

def GetBookContent(filename, md5, file_type):
    params = {"filename": filename, "hash":md5, "type": file_type}
    r = requests.get(UPLOAD_HOST + '/get', params=params)
    r.encoding = "utf-8"
    return r.content


class BookDetailsHandler(BaseHandler):
    """书籍详情
    """
    async def get(self):
        self.set_secure_cookie('info', 'msg')
        sefl.set_default_headers()
        results = await self.query(
        'SELECT * FROM public."books"'
        )
        if not results:
            self.write("<h3>oops, you have no book</h3>")
        self.render("test.html",
                books = results,
                title = "test")
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", self.request.headers.get("Origin", ""))
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,authorization")
        self.set_header("Access-Control-Allow-Methods", "POST,GET")
        self.set_header("Access-Contrrol-Allow-Credentias", "true")

class BookSendHandler(BaseHandler):
    """kindle书籍推送
    """
    async def get(self):
        self.write("oops, 404")
        self.flush
        return

    async def post(self):
        import json
        self.get_secure_cookie("info")

        book_id = self.get_argument('book_id', '')
        to_addr = self.get_argument('to', '')
        logging.info(to_addr)
        logging.info(book_id)

        if book_id and to_addr:
            sqlstr = """SELECT * FROM "books" as B WHERE B.id = %s"""
            logging.info("正在查询..")
            result = await self.queryone(sqlstr, int(book_id))
            logging.info("书籍查询完毕，正在提取")
            book_content = GetBookContent(result['title'], reuslt['path'], result['format'])
            logging.info("book 内容获取完毕！")
            sendemail.send(to_addr, book_content, result['title'])
            self.write(json.dumps({"status", '200'}))
            self.flush()
            return
        self.write("send to kindle field!")
        self.flush()

            

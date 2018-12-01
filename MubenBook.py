# 图书详情页面
# 图书推送功能
import requests
from BaseHandler import *
import logging
from utils.smtp import *


class BookDetailsHandler(BaseHandler):
    """书籍详情
    """
    async def get(self):
        results = await self.query(
        'SELECT * FROM public."books"'
        )
        if not results:
            self.write("<h3>oops, you have no book</h3>")
        self.render("test.html",
                books = results,
                title = "test")


class BookSendHandler(BaseHandler):
    """kindle书籍推送
    """
    async def get(self):
        self.write("oops, 404")
        self.flush
        return

    async def post(self):
        import json
        book_id = self.get_argument('_val', '')
        to_addr = self.get_argument('To', '')
        if book_id and to_addr:
            sqlStr = """SELECT * FROM "books" as B WHERE B.id == %s"""
            result = await self.queryone(sqlstr, book_id)
            sendemail.send(to_addr, result['path'], result['title'])
            self.write(json.dumps({"status", '200'}))
            self.flush()
            return
        self.write("send to kindle field!")
        self.flush()

            

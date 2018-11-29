import tornado.web
import tornado.ioloop
import tornado.httpserver
import os

class IndexHandler(tornado.web.RequestHandler):
    async def get(self):
        self.render("index.html")


class UploadHandler(tornado.web.RequestHandler):
    # tornado.httputil.HTTPFile
    # 1. filename
    # 2. body
    # 3. type
    async def get(self, *args, **kwargs):
        self.write("404")

    async def post(self, *args, **kwargs):
        filesDict = self.request.files
        for inputname in filesDict:
            http_file = filesDict[inputname]
            for meta in http_file:
                file_name = meta['filename']
                filePath = os.path.join(os.path.dirname(__file__), file_name)
                print(filePath)
                with open(filePath, 'wb') as f:
                    f.write(meta['body'])
        self.write("上传成功！")

settings = {
    "template_path": 'views',
    "static_path": "static",
}

if __name__ == "__main__":
    app = tornado.web.Application(
            [(r"/fileupload", UploadHandler),
                (r"/", IndexHandler)]
            , **settings)
    httpserver = tornado.httpserver.HTTPServer(app)
    httpserver.bind(8000)
    httpserver.start()
    tornado.ioloop.IOLoop.instance().start()

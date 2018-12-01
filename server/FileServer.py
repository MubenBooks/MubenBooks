import hashlib
import tornado.web
import tornado.gen
import tornado.ioloop
import tornado.httpserver
import os
import logging

from tornado.options import define, options, parse_command_line

"""
    todos: 1.当使用chrome下载时，会出现闪退的情况
    2.当出现大并发需求时，如何提高效率
"""



define("book_root_path", default=os.path.join(os.path.dirname(__file__), 
    'ebooks'), help = "default book store path")
define("port", default = 7000, help = "run on defaul given port", type=int) 


class FileSystem:
    """File Operations

    """

    def __init__(self):
        self.initialize()
        self.if_no_ebooks()

    def initialize(self):
        self.root = options.book_root_path

    def if_no_ebooks(self):
        # ebooks 文件夹不存在时创建文件夹
        if not os.path.exists('ebooks'):
            return self.mkdir(options.book_root_path, '')
    def is_exists(self, path):
        return os.path.exists(path)

    def mkdir(self, root, dirname):
        """Create directory by root path and dirname
            
            Return the created dirctory path
        """
        try:
            path = os.path.join(root, dirname)
            if self.is_exists(path):
                path
            else:
                os.mkdir(path)
            return path
            # tornado.gen.Return(os.path.join(root, dirname))
        except FileExistsError as e:
            logging.warning("Directory already exists, no need for create")
        return

    def GetPathByHash(self, md5):
        try:
            # path = self.root
            # for item in [md5[:2], md5[-2:]]:
            #     path = os.path.join(path, item)
            path = os.path.join(os.path.join(self.root, md5[:2]), md5[-2:])
            return path
            # raise tornado.gen.Return(path)
        except IndexError as e:
            logging.error(e)

    def file_extension(self, postfix):
        """预处理后缀名称
            
            返回处理过的后缀 (例如： 传入的参数是'bat', 返回的参数是 '.bat')）
            如果已经是最终格式，则直接返回
        """
        # 如果有 '/'非法字符，则去掉
        try:
            fix = postfix if postfix.startswith('.') else str('.' + postfix)
            return fix
        except Exception as e:
            logging.error(e)
            return


class Encrypt:
    """Read file and return the 16-bits hash
        
        in
    """
    def md5(self, FileContent):
        """Calculate hash MD5 value by the path file
            
            @param File path
        """
        try:
            md5Obj = hashlib.md5()
            md5Obj.update(FileContent)
            hash_md5 = md5Obj.hexdigest()
            return hash_md5
        except Exception as e:
            logging.error(e)
            return

# Create Object
file = FileSystem()
encrypt = Encrypt()



class IndexHandler(tornado.web.RequestHandler):
    """
        根据文件散列提取文件
    """

    def get(self):
        filename = self.get_argument("filename", '')
        file_hash = self.get_argument("hash", "")
        file_type = self.get_argument("type", "")

        logging.info("filename is: " + filename)
        logging.info("file hash is: " + file_hash)
        logging.info("file type is: " + file_type)

        CHUNK_SIZE = 512000         # 0.5 MB
        
        # 文件名或者文件MD5值为空
        if not filename or not file_hash:
            self.write("请输入文件名参数再尝试!!!")
            self.flush()
            return

        # 生成文件路径
        self.path = os.path.join(file.GetPathByHash(file_hash),
         file_hash + file.file_extension(file_type))


        # 设置文档类型， 告诉浏览器把它当文件下载
        self.set_header('Content-Type', 'application/octet-stream; charset=utf-8')
        self.set_header('Content-Length', os.path.getsize(self.path))
        # 设置文件下载时使用的名称
        self.set_header('Content-Disposition', 
            ('attachment; name="%s"; filename="%s"' 
                % (filename, filename + file.file_extension(file_type))
            )
        )

        try:
            # 根据hash值获取前两层文件夹地址
            # 获取文件夹地址后和文件名合并
            with open(self.path, 'rb') as f:
                while True:
                    data = f.read(CHUNK_SIZE)
                    if not data:
                        break
                    # 发送文件碎片
                    self.write(data)
                    self.flush()
            # 结束文件发送
            self.finish()
        except Exception as e:
            logging.error("读取文件失败...")
            self.write("读取文件失败!")
            self.flush()


class UploadHandler(tornado.web.RequestHandler):
    # tornado.httputil.HTTPFile
    # 1. filename
    # 2. body
    # 3. type
    async def get(self, *args, **kwargs):
        self.write("404")

    def post(self, *args, **kwargs):
        filesDict = self.request.files
        for inputname in filesDict:
            http_file = filesDict[inputname]
            for meta in http_file:
                postfix = os.path.splitext(meta['filename'])[-1]

                # 计算文件散列值
                file_md5 = encrypt.md5(meta['body'])
                logging.info("file md5: " + file_md5)
                if not file_md5 and file_md5 is not str:
                    self.write("上传文件失败，请重试!!!")

                # 两级目录，一级为MD5前两位， 二级为MD5 后两位
                try:
                    # 根据散列创建文件夹
                    file_dir = file.mkdir(file.mkdir(options.book_root_path,file_md5[:2]), file_md5[-2:])
                except IndexError as e:
                    # 处理越界错误
                    logging.error("File MD5 index out of range...")
                    self.write("upload file faield, please try again.<br>If it still happened, please contact website administor")
                    self.flush()
                    return

                filePath = os.path.join(file_dir, file_md5 + postfix)

                # 写入本地
                # 如果文件已经存在则覆盖文件
                logging.info("file path: " + filePath)
                with open(filePath, 'wb') as f:
                    f.write(meta['body'])
        self.write("上传成功！")


class TestHandler(tornado.web.RequestHandler):

    async def get(self):
        self.render("index.html")


settings = dict(
    template_path = 'views',
    static_path = 'static',
    debug = True,
)

if __name__ == "__main__":
    parse_command_line()

    app = tornado.web.Application(
            [(r"/upload", UploadHandler),
                (r"/get", IndexHandler),
                (r"/", TestHandler)]
            , **settings)
    app.listen(options.port)
    # httpserver = tornado.httpserver.HTTPServer(app)
    # httpserver.bind(8000)
    # httpserver.start()
    tornado.ioloop.IOLoop.current().start()

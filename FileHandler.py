import hashlib
import tornado.gen
import logging
# import types
import os

from tornado.options import options
from utils.smtp import *
from BaseHandler import *

"""
    todos: 1.当使用chrome下载时，会出现闪退的情况
    2.当出现大并发需求时，如何提高效率
"""

book_root_path = os.path.join(os.path.dirname(__file__),  'ebooks')


class FileSystem:
    """File Operations

    """

    def __init__(self):
        self.initialize()
        self.if_no_ebooks()

    def initialize(self):
        self.root = book_root_path

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



class MailBook:
    @tornado.gen.coroutine
    def send(self, to_addr, info):
        """从本地发送文件

            @to_addr: 接收方地址
            @info: 电子书数据

            @return:
                return True if successfully, else return False
        """
        try:
            filename = info['title']
            filehash = info['path']
            filetype = info['format']
        except IndexError as e:
            logging.error(e)
            return False

        # 生成文件路径
        path = os.path.join(file.GetPathByHash(filehash),
         filehash + file.file_extension(filetype))

        try:
            with open(path, 'rb') as fb:
                book_content = fb.read()
        except:
            logging.warning("read book file from local failed...")
            return

        status = sendemail.send(to_addr, book_content, filename)
        raise tornado.gen.Return(status)

# Create Object
file = FileSystem()
encrypt = Encrypt()
mailbook = MailBook()


class UploadBookHandler(BaseHandler):
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


class TestHandler(BaseHandler):

    async def get(self):
        self.render("files.html")


if __name__ == "__main__":
    # parse_command_line()

    # app = tornado.web.Application(
    #         [(r"/upload", UploadHandler),
    #             (r"/get", IndexHandler),
    #             (r"/", TestHandler)]
    #         , **settings)
    # app.listen(options.port)
    # # httpserver = tornado.httpserver.HTTPServer(app)
    # # httpserver.bind(8000)
    # # httpserver.start()
    # tornado.ioloop.IOLoop.current().start()
    pass

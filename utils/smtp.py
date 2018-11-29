# kindle 电子书推送支持模块
import smtplib
import ConfigParser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



class SendEmail:
    """Senf email module"""
    def __init__(self):
        self.initialize()

    def initialize(self):
        conf = ConfigParser.ConfigParser()
        conf.read('../conf/smtp.conf')
        self.server = conf.get('smtp', 'server')
        self.port = conf.get('smtp', 'port')
        self.password = conf.get('smtp', 'password')
        self.from_addr = conf.get('smtp', 'from_addr')

    def send(self, To, path, title):
        """send email to 'To'

        param: To  --The destination email address
               path --send file path
               title --send file name
        """
        content = "Kindle推送服务"
        
        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['Subject'] = title
        message['From']    = self.from_addr
        message['To']      = ";".join(To)

        # 邮件正文
        message.attach(MIMEText(content, 'plain', 'utf-8'))

        # 构造附件
        try:
            with open(path, 'rb') as fb:
                fbfile = fb.read()
                att = MIMEText(fbfile, 'base64', 'utf-8')
                att['Content-Type'] = 'application/octet-stream'
                att['Content-Disposition'] = 'attachment; filename="{0}"'.format(title)
                message.attach(att)
        except Exception as e:
            logging.warning(e)
            return
        
        try:
            server = smtplib.SMTP_SSL()
            server.connect(self.server, self.port)
            server.login(self.from_addr, self.password)
            server.sendmail(self.from_addr, To, message.as_string())
        except Exception as e:
            logging.warning(e)
        finally:
            server.close()
            return

sendemail = SendEmail()

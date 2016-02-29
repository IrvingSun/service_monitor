#!encoding=UTF-8
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

from email.mime.text import MIMEText
import smtplib


def send_email(messge='test', sub='监控', toList=['huji@le.com']):
    smtp_server = 'smtp.163.com'
    mail_user = 'lszxit_monitor@163.com'
    password = 'lszxit'

    # 创建一个实例，这里设置为html格式邮件
    msg = MIMEText(messge, _subtype='html', _charset='utf-8')
    msg['From'] = _format_addr('系统监控程序 <' + mail_user + '>')
    msg['To'] = ",".join(toList)
    msg['Subject'] = Header(sub, 'utf-8').encode()
    try:
        server = smtplib.SMTP()
        server.connect(smtp_server)  # 连接smtp服务器
        server.login(mail_user, password)  # 登陆服务器
        server.ehlo()
        server.starttls()
        # server.set_debuglevel(1)
        server.sendmail(mail_user, toList, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print e
        return False


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((
        Header(name, 'utf-8').encode(),
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

import poplib
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
# -------------------------------------------------
#
# Utility to read email from QQ Using Python
#
# ------------------------------------------------

SMTP_SERVER = "imap.gmail.com"
SERVER = "pop.qq.com"

def get_qqmail_pop(user, pwd):
    server = poplib.POP3_SSL(SERVER)
    server.user(user)
    server.pass_(pwd)

    emails = []
    resp, mails, octets = server.list()
    index = len(mails)
    for i in range(len(mails)):
        resp, lines, octets = server.retr(i + 1)

        msg_content = b'\r\n'.join(lines)
        msg_content = msg_content.decode()
        msg = Parser().parsestr(msg_content)

        email_data = {}
        email_data['header'] = get_email_header(msg)
        email_data['content'] = get_email_content(msg)
        emails.append(email_data)
        server.dele(i + 1) # delete email

    server.quit()
    return emails

def get_email_header(msg, indent=0):
    results = {}
    if indent == 0:
        # 邮件的From, To, Subject存在于根对象上:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    # 需要解码Subject字符串:
                    value = decode_str(value)
                else:
                    # 需要解码Email地址:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            results[header] = value
        return results

def get_email_content(msg, indent=0):
    contents = []
    def get_content(msg, indent=0):
        if (msg.is_multipart()):
            # 如果邮件对象是一个MIMEMultipart,
            # get_payload()返回list，包含所有的子对象:
            parts = msg.get_payload()
            for n, part in enumerate(parts):
                # 递归打印每一个子对象:
                get_content(part, indent + 1)
        else:
            # 邮件对象不是一个MIMEMultipart,
            # 就根据content_type判断:
            content_type = msg.get_content_type()
            if content_type=='text/plain' or content_type=='text/html':
                # 纯文本或HTML内容:
                content = msg.get_payload(decode=True)
                # 要检测文本编码:
                charset = guess_charset(msg)
                if charset:
                    content = content.decode(charset)
                contents.append(content)
            else:
                # 不是文本,作为附件处理:
                print('%sAttachment: %s' % ('  ' * indent, content_type))
    get_content(msg)
    return contents

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def guess_charset(msg):
    # 先从msg对象获取编码:
    charset = msg.get_charset()
    if charset is None:
        # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

from email.mime.multipart import MIMEMultipart
from email.mime.message import MIMEMessage
from email.mime.text import MIMEText
from email.utils import getaddresses
from smtplib import SMTP

SMTP_SERVER = 'alpha.xerox.com'


class TextMail(MIMEText):
    def __init__(self, **headers):
        MIMEText.__init__(self, '')

        for header in headers:
            dest = header.lstrip('_').replace('_','-')
            self[dest] = headers[header]

    def containing(self, body):
        self.set_payload(body)

        return self

class HTMLMail(MIMEText):
    def __init__(self, **headers):
        MIMEText.__init__(self, '', 'html')

        for header in headers:
            dest = header.lstrip('_').replace('_','-')
            self[dest] = headers[header]

    def containing(self, body):
        self.set_payload(body)

        return self

class Multipart(MIMEMultipart):
    def __init__(self, subtype, **headers):
        MIMEMultipart.__init__(self, subtype)

        for header in headers:
            dest = header.lstrip('_').replace('_','-')
            self[dest] = headers[header]

    def containing(self, *messages):
        for msg in messages:
            self.attach(msg)
        
        return self


def send(msg):
    server = SMTP(SMTP_SERVER)
    server.set_debuglevel(1)

    fromaddr = msg['from']

    tos = msg.get_all('to', [])
    ccs = msg.get_all('cc', [])
    bccs = msg.get_all('bcc', [])
    toaddrs = [email for name,email in getaddresses(tos + ccs + bccs)]

    server.sendmail(fromaddr,toaddrs,msg.as_string())
    server.quit()

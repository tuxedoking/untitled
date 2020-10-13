import poplib
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def sendqqmail():
    sender = '387889277@qq.com'
    receivers = ['387889277@qq.com']
    message = MIMEText('zhouli01@feidai.com 有新邮件', 'plain', 'utf-8')
    message['From'] = Header('tuxedo', 'utf-8')
    message['To'] = Header('tuxedo', 'utf-8')
    subject = 'zhouli01@feidai.com 新邮件提醒'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP('smtp.qq.com')
        smtpObj.starttls()
        smtpObj.login('387889277@qq.com', 'xknisilujlzgbibi')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print('邮件发送成功')
    except smtplib.SMTPException:
        print('Error: 无法发送邮件')


def receive_emails(pop3_server, user_name, passwd, server_port):
    try:
        pop_client = poplib.POP3(pop3_server, port=server_port)
        pop_client.user(user_name)
        pop_client.pass_(passwd)

        num_messages, mbox_size = pop_client.stat()
        return num_messages
    except:
        return


if __name__ == '__main__':
    lastmailnum = 0
    while True:
        mailnum = receive_emails('172.16.4.78', 'zhoul01@feidai.com', 'zxwd000.', 110)
        print('there are %d new emails,lastnum = %d' % (mailnum, lastmailnum))
        if mailnum != lastmailnum:
            if lastmailnum == 0:
                lastmailnum = mailnum
            else:
                sendqqmail()
                lastmailnum = mailnum
        time.sleep(10)

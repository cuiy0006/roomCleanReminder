import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

CONTACTS = []
with open('config.txt') as contacts_handler:
    for line in contacts_handler.readlines():
        name, email = line.split(',')
        email = email.replace('\n', '')
        CONTACTS.append((name, email))

INDEX = -1
with open('turn.txt') as turn_handler:
    for line in turn_handler.readlines():
        INDEX = int(line)

CURRENT_INDEX = INDEX
CURRENT_NAME, CURRENT_EMAIL = CONTACTS[CURRENT_INDEX]
if INDEX == len(CONTACTS)-1:
    INDEX = 0
else:
    INDEX += 1

with open('turn.txt', 'w') as writer_handler:
    writer_handler.write(str(INDEX)) 

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

#CONTACTS = [('CY1', 'yc2554@nyu.edu'), ('CY2', 'cuiy0006@gmail.com'), ('CY3', 'cuiy0006@outlook.com')]

FROM_ADDR = 'cuiy0006@outlook.com'
PASSWORD = 'Eat1Apple!'
TMP = [email for name, email in CONTACTS]
TO_ADDR = ','.join(TMP)
STMP_SERVER = 'smtp-mail.outlook.com'

TEXT = ' It is ' + CURRENT_NAME + ' \'s turn to clean room next week.\n This email is automatically generated as a reminder every weekend so cannot be guaranteed. \n '
MSG = MIMEText(TEXT, 'plain', 'utf-8')
MSG['From'] = _format_addr('YAO CUI <%s>' % FROM_ADDR)
TMP = [_format_addr(name + ' <%s>' % email) for name, email in CONTACTS]
MSG['To'] = ','.join(TMP)
MSG['Subject'] = Header('Room Clean Reminder', 'utf-8').encode()

SERVER = smtplib.SMTP(STMP_SERVER, 587)
SERVER.ehlo()
SERVER.starttls()
SERVER.set_debuglevel(1)
SERVER.login(FROM_ADDR, PASSWORD)
SERVER.sendmail(FROM_ADDR, [TO_ADDR], MSG.as_string())
SERVER.quit()

print(CURRENT_NAME)
print(CURRENT_EMAIL)
input('hi')

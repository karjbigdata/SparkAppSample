import imaplib, ssl, email, os
from pathlib import Path
from getpass import getpass

FOLDER_PATH = r'D:\BigData_Practice\pyspark_work\SparkAppSample\EmailOutputData'

# Email details, Read this data from config file
email_user = "karthikeyy@outlook.com"
email_password = "Apple@098426"
#email_password = getpass()

context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
mail = imaplib.IMAP4_SSL("imap-mail.outlook.com", port=993, ssl_context=context)

# Login to email
mail.login(email_user, email_password)
print("login success to email account!!!")
#Select Inbox folder
mail.select('Inbox')

type, data = mail.search(None, "ALL")
mail_ids = data[0]
print('maild_ids ', mail_ids)

id_list = mail_ids.split()

print('id _lst is ', id_list)
# print(data[0].decode('utf8').split(' '))
decoded_data = data[0].decode('utf8')
print('data dtype is ', decoded_data)

for response_part in data:
    print('response_part', response_part)
    if isinstance(response_part, tuple):
        print('inside')
        msg = email.message_from_string(response_part[1].decode('utf-8'))
        email_subject = msg['subject']
        email_from = msg['from']
        print('From : ' + email_from + '\n')
        print('Subject : ' + email_subject + '\n')
        print(msg.get_payload(decode=True))

#
# mylist = []
#
# for id in data[0].split():
#     type, data = mail.fetch(id, '(RFC822)')
#     raw_email = data[0][1]
#     #Convert byte literal to String removing b
#     raw_email_string = raw_email.decode('utf-8')
#     email_message = email.message_from_string(raw_email_string)
#     # download attachments
#     for part in email_message.walk():
#         if part.get_content_maintype() == 'multipart':
#             continue
#         if part.get('Content-Disposition') is None:
#             continue
#         fileName = part.get_filename()
#         print("id is ", id)
#         if id in mylist:
#             pass
#         else:
#             mylist.append(id)
#         if bool(fileName):
#             sender = email_message['From']
#             sender = sender.replace('<', '')
#             sender = sender.replace('>', '')
#             tpath = FOLDER_PATH + '\\' + str(sender)
#             Path(tpath).mkdir(parents=True, exist_ok=True)
#             filePath = os.path.join(tpath, fileName)
#             if not os.path.isfile(filePath):
#                 fp = open(filePath, 'wb')
#                 fp.write(part.get_payload(decode=True))
#                 fp.close()
#             subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
#             print(tpath)
#             print('Downloaded "{file}" from email titled "{subject}".'.format(file=fileName,
#                                                                               subject=subject))  # , uid=mail.uid.decode('utf-8')))
# for i in mylist:
#     mail.copy(i, 'INBOX.Processed')
#     mail.store(i, '+FLAGS', '\\Deleted')
# mail.expunge()
#
#
#
#
#
#
#
#
#
#
#

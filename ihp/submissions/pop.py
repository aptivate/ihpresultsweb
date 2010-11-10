import poplib
import email
import mimetypes
from tempfile import NamedTemporaryFile
from django.conf import settings
from helpers import parse_file

def pop_feed(username, password, host):
    try:
        pop = poplib.POP3_SSL(host)
        pop.user(username)
        pop.pass_(password)
        list = pop.list()
        num_messages = len(pop.list()[1])

        for i in range(num_messages):
            message = "\n".join(pop.retr(i + 1)[1])
            fp = open("test_message.txt", "wb")
            fp.write(message)
            fp.close()
            email_message = email.message_from_string(message)
            yield email_message
    finally:
        pop.quit()

def disk_feed():
    message = open("test_message.txt").read()
    email_message = email.message_from_string(message)
    yield email_message

def grab_messages(message_source):

    messages = []
    counter = 0

    for email_message in message_source:
        message_dict = dict(email_message.items())
        files = message_dict["files"] = []
        messages.append(message_dict)

        if email_message.is_multipart():
            for part in email_message.walk():
                # multipart/* are just containers
                if part.get_content_maintype() == "multipart":
                    continue
                elif part.get_content_type() == "text/plain":
                    text_body = part.get_payload(decode=True)
                    message_dict["text_body"] = text_body
                elif part.get_content_type() == "text/html":
                    html_body = part.get_payload(decode=True)
                    message_dict["html_body"] = html_body
                else:
                    filename = part.get_filename()
                    if not filename:
                        ext = mimetypes.guess_extension(part.get_content_type())
                        if not ext:
                            # Use a generic bag-of-bits extension
                            ext = ".bin"
                        filename = "part-%03d%s" % (counter, ext)
                    counter += 1
                    fp = NamedTemporaryFile(delete=False)
                    fp_name = fp.name
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                    files.append((fp_name, filename))
        else:
            if email_message.get_content_type() == "text/plain":
                text_body = email_message.get_payload(decode=True)
                message_dict["text_body"] = text_body
            elif email_message.get_content_type() == "text/html":
                html_body = email_message.get_payload(decode=True)
                message_dict["html_body"] = html_body
    return messages

def poll():
    pop_messages = pop_feed(
        settings.POLL_USERNAME, 
        settings.POLL_PASSWORD, 
        settings.POLL_HOST
    ) 
    #pop_messages = disk_feed() 
    messages = grab_messages(pop_messages)
    for message in messages:
        try:
            print "Processing messing"
            for (filename, original_filename) in message["files"]:
                parse_file(filename)
        except Exception, e:
            print e

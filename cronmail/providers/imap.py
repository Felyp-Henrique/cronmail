import re
import imaplib
import email
from email.header import decode_header
from typing import Iterator


def imap_connect(host: str, **kwargs) -> imaplib.IMAP4:
    """
    Get a new connection for IMAP Server.

    Args:
        host (str): The address for IMAP Server.

    Keyword Args:
        port (int): The port for IMAP Server.
        ssl_on (bool): Enable the SSL connection.
    """
    ssl_on = kwargs.get('ssl_on', False)
    port = kwargs.get('port', (143 if not ssl_on else 993))
    if ssl_on:
        return imaplib.IMAP4_SSL(host=host, port=port)
    else:
        return imaplib.IMAP4(host=host, port=port)


def imap_auth_login(connection: imaplib.IMAP4, username: str, password: str) -> bool:
    """
    Do login in IMAP Connection.

    Args:
        connection (imaplib.IMAP4 | imaplib.IMAP4_SSL): A IMAP connection server.
        username (str): The user's email.
        password (str): The user's password.
    """
    ok, _ = connection.login(username, password)
    return ok == 'OK'


def imap_auth_logout(connection: imaplib.IMAP4) -> bool:
    """
    Do logout in IMAP connection.
    """
    bye, _ = connection.logout()
    return bye == "BYE"


def imap_mailbox_get_list(connection: imaplib.IMAP4) -> Iterator[str]:
    """
    Get the list of mailbox.

    Args:
        connection (imaplib.IMAP4 | imaplib.IMAP4_SSL): A IMAP connection server.
    """
    for mailbox in connection.list()[1]:
        if isinstance(mailbox, bytes):
            mailbox = mailbox.decode('UTF-8')
        mailbox_metainfos = mailbox.split('"/"')
        mailbox_name = mailbox_metainfos[-1]
        mailbox_name = mailbox_name.replace("\"", "")
        yield mailbox_name


def imap_mailbox_set_inbox(connection: imaplib.IMAP4, mailbox: str = "INBOX") -> None:
    """
    Define the INBOX target to do any operation.

    Args:
        connection (imaplib.IMAP4 | imaplib.IMAP4_SSL): A IMAP connection server.
        mailbox (str): The mailbox's name.
    """
    connection.select(mailbox)


def imap_emails_get_senders(connection: imaplib.IMAP4) -> Iterator[str]:
    """
    Get list of Sender in mailbox emails.

    Args:
        connection (imaplib.IMAP4 | imaplib.IMAP4_SSL): A IMAP connection server.
    """
    email_regexp = re.compile(r".*(<(?P<email>.*)>).*")
    for email_id in connection.search(None, 'ALL')[1][0].split():
        _, email_content  = connection.fetch(email_id, "(RFC822)")
        for email_content_response in email_content:
            if not isinstance(email_content_response, tuple):
                continue
            email_content_message = email.message_from_bytes(email_content_response[1])
            email_content_from, _ = decode_header(email_content_message.get("From"))[-1]
            if isinstance(email_content_from, bytes):
                email_content_from = email_content_from.decode('utf-8')
            email_sender_search = email_regexp.search(email_content_from)
            if email_sender_search is None:
                break
            else:
                yield email_sender_search.group("email")
            break

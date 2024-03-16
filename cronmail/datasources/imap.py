import imaplib
import email
from email.header import decode_header
from typing import Iterator


class IMAPDataSource:
    """
    IMAP Data Source.
    """

    def __init__(self, host: str, port: int = None, ssl_on: bool = False) -> None:
        if ssl_on:
            self.__connection = imaplib.IMAP4_SSL(
                host=host,
                port=(port if not port is None else 993),
            )
        else:
            self.__connection = imaplib.IMAP4(
                host=host,
                port=(port if not port is None else 143),
            )

    def do_login(self, username: str, password: str) -> list:
        self.__connection.login(username, password)

    def get_senders(self) -> Iterator[str]:
        self.__connection.select('INBOX')
        emails_ids = self.__connection.search(None, 'ALL')[1][0].split()
        for email_id in emails_ids:
            _, email_content  = self.__connection.fetch(email_id, "(RFC822)")
            for email_content_response in email_content:
                if not isinstance(email_content_response, tuple):
                    continue
                email_content_message = email.message_from_bytes(email_content_response[1])
                email_content_from, _ = decode_header(email_content_message.get("From"))[-1]
                if isinstance(email_content_from, bytes):
                    yield email_content_from.decode('utf-8')
                else:
                    yield email_content_from
                break

if __name__ == "__main__":
    imap = IMAPDataSource('imap.gmail.com', ssl_on=True)
    imap.do_login("<username>", "<password>")
    for email_ in imap.get_senders():
        print(email_)

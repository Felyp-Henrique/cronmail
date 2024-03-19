import click
from rmail.providers import imap
from . import rmail


@rmail.group(name="gmail")
@click.pass_context
def gmail(context) -> None:
    """
    Collection of commands to handle Gmail's mails.
    """
    context.connection = imap.imap_connect("imap.gmail.com", ssl_on=True)


@gmail.command(name="senders:list")
@click.argument("username")
@click.option("--password", "-p")
@click.pass_context
def gmail_senders_list(context, username: str, password: str) -> None:
    """
    Show the list of senders.
    """
    if not imap.imap_auth_login(context.connection, username, password):
        return
    for sender_email in imap.imap_emails_get_senders(context.connection):
        click.echo(sender_email)

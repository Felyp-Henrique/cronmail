import click
from rmail.providers import imap
from . import rmail


@rmail.group(name="gmail")
@click.option("--no-warn", "-w", 'warn_on', is_flag=True, default=False)
@click.pass_context
def gmail(context, warn_on: bool) -> None:
    """
    Collection of commands to handle Gmail's mails.
    """
    context.warn_on = warn_on
    context.connection = imap.get_connection("imap.gmail.com", ssl_on=True)


@gmail.command(name="senders")
@click.argument("username")
@click.option("--password", "-p", required=True)
@click.option("--mailbox", "-m", default=None)
@click.pass_context
def gmail_senders(context, username: str, password: str, mailbox: str) -> None:
    """
    Show the list of senders.
    """
    was_showed = set()
    if not context.parent.warn_on:
        click.secho("It's can take some time!", fg="yellow", bold=True)
    if not imap.do_login(context.parent.connection, username, password):
        return
    if mailbox is None:
        imap.set_mailbox(context.parent.connection, "INBOX")
    else:
        imap.set_mailbox(context.parent.connection, mailbox)
    for _, sender_email in imap.get_senders(context.parent.connection):
        if sender_email in was_showed:
            continue
        else:
            was_showed.add(sender_email)
        click.echo(sender_email)


@gmail.command(name="senders:delete")
@click.argument("username")
@click.argument("sender")
@click.option("--password", "-p", required=True)
@click.option("--mailbox", "-m", default=None)
@click.pass_context
def get_senders_delete(context, username: str, sender: str, password: str, mailbox: str) -> None:
    """
    Remove all emails about the sender.
    """
    if not context.parent.warn_on:
        click.secho("It's can take some time!", fg="yellow", bold=True)
    if not imap.do_login(context.parent.connection, username, password):
        return
    if mailbox is None:
        imap.set_mailbox(context.parent.connection, "INBOX")
    else:
        imap.set_mailbox(context.parent.connection, mailbox)
    for email_id, sender_email in imap.get_senders(context.parent.connection, search=sender):
        imap.email_delete(context.parent.connection, email_id)
        click.echo(f"Email with id '{ int(email_id) }' from '{ sender_email }' was deleted!")

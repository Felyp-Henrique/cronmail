import click


@click.group(name="rmail")
@click.option("--debug", "-d", default=False)
@click.pass_context
def rmail(context, debug: bool) -> None:
    """
    The main command.
    """
    context.debug = debug

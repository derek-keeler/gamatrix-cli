"""
Gamatrix-cli

Command line interface for Gamatrix.
"""

import json
from typing import List

import click

import gamatrixcli.constants as const
from gamatrixcli.config import GMCLIConfig

# We need to do the following operations:
# 1. Import a DB from a user.
#   1.a. Parse the DB, pulling out what we need.
#   1.b. Storing the necessary information in our own data store.
# 2. Compare DBs between any combination of users.
#   2.a. For each comparison, cache the results so we don't calculate it again.
# 3. Show all games owned by a single user.


@click.group()
@click.pass_context
@click.option(
    "--config-file",
    "-c",
    help=(
        "The path to the configuration file. If the configuration "
        "file is not found, the default configuration will be used."
    ),
    type=click.Path(),
    default=const.DEFAULT_CONFIG_PATH,
)
def gcli(ctx: click.Context, config_file: click.Path) -> None:
    if config_file.exists():
        with open(config_file, "r") as cf:
            config = json.loads(cf)
            conf = GMCLIConfig(config)
    else:
        conf = GMCLIConfig(conf.get_default_config())

    # pass the config object to subordinate commands
    ctx.ensure_object(dict)
    ctx.obj["config"] = conf


@gcli.command()
@click.pass_context
@click.option(
    "--db", prompt="Enter the path to the DB file", help="The path to the DB file."
)
@click.option("--user", prompt="Enter the user name", help="The user name.")
def add_db(ctx: click.Context, db: click.Path, user: str) -> None:
    """Adds a new database for a user to gamatrix.

    If the user isn't yet known to gamatrixcli, the database is added
    and the user incorporated into the gamatrixcli's data store. If the
    user is known to gamatrixcli, the database is stored into the user's
    data store within gamatrix and their games and metadata is updated with
    the new information.

    Note: Gamatrixcli stores the 3 most recent DBs as the user's 'raw data'
    as a backup in case of data corruption.
    """
    print(f"Adding database file {db} for user {user}")
    # print(f"The database pertains to this user: {user}")
    conf: GMCLIConfig = ctx.obj["config"]
    conf.add_db(user_db_file=db, user=user)


@gcli.command()
@click.option(
    "--user",
    prompt="Enter the user name",
    help=(
        "The user name to include in the comparison, if none "
        "are specified then compare all users."
    ),
    multiple=True,
)
@click.option(
    "--installed-only",
    is_flag=True,
    help="Only compare between user's installed games.",
)
@click.option(
    "--game-service",
    prompt="Enter the game services to compare games from",
    help="The game service to show games from. If not specified, all game services will be shown",
)
def compare(user: List[str]) -> str:
    """Compare the games owned between users.

    If no users are specified, compare all users. Optionally
    compare only games installed for all users being compared,
    and from which service the games are provided by.
    """

    print("Comparing the following users: {user}")

    return ""


@gcli.command()
@click.option("--user", prompt="Enter the user name", help="The user name.")
def show(user: str) -> str:
    """Show everything Gamatrix knows about a user.

    Include the list of all games the user owns, and the
    installation status of each.
    """
    print(f"Showing games for user {user}")
    return ""


if __name__ == "__main__":
    gcli()

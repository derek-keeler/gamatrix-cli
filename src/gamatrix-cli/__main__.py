"""
Gamatrix-cli

Command line interface for Gamatrix.
"""

from typing import List

import click

# We need to do the following operations:
# 1. Import a DB from a user.
#   1.a. Parse the DB, pulling out what we need.
#   1.b. Storing the necessary information in our own data store.
# 2. Compare DBs between any combination of users.
#   2.a. For each comparison, cache the results so we don't calculate it again.
# 3. Show all games owned by a single user.


@click.group()
def gcli() -> None:
    pass


@gcli.command()
@click.option(
    "--db", prompt="Enter the path to the DB file", help="The path to the DB file."
)
@click.option("--user", prompt="Enter the user name", help="The user name.")
def add_db(db: click.Path, user: str) -> bool:
    """Add or update a users DB to gamatrix."""
    print("Adding database file {db}")
    print("The database pertains to this user: {user}")

    return False


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

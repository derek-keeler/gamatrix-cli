"""Various constants/default values used by gamatrix."""

from pathlib import Path

DEFAULT_DATASTORE_PATH = Path.home().joinpath(".gamatrix")
DEFAULT_CONFIG_PATH = DEFAULT_DATASTORE_PATH.joinpath("gamatrixcli.config")
DEFAULT_DB_PATH = DEFAULT_DATASTORE_PATH.joinpath("gamatrix.db")
DEFAULT_USER_DB_PATH = DEFAULT_DATASTORE_PATH.joinpath("user_dbs")

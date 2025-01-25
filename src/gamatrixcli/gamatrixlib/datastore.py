"""datastore: module that handles the main gamatrix data store."""

from pathlib import Path
import sqlite3
from typing import Dict, List

import gamatrixcli.constants as constants
from gamatrixcli.gamatrixlib.rawdb import RawDB
from gamatrixcli.gamatrixlib.config import GMConfig


class GamatrixDataStore:
    """The main data store for gamatrix."""

    def __init__(self, user_dbs: List[RawDB], config: GMConfig, db: sqlite3.Connection):
        self._db: sqlite3.Connection = db
        self._config: GMConfig = config
        self._user_dbs: Dict[str, List[RawDB]] = {}
        for rawdb in user_dbs:
            user = rawdb.user
            if user not in self._user_dbs:
                self._user_dbs[user] = []
            self._user_dbs[user].append(rawdb)

    def add_db(self, db_file: RawDB) -> None:
        """Add a new database file to the data store.

        The data store within gamatrix and their games and metadata is updated with
        the new information.

        Note: Gamatrixcli stores the 3 most recent DBs as the user's 'raw data'
        as a backup in case of data corruption.
        """
        if db_file.user in self._user_dbs:
            self._user_dbs[db_file.user].append(db_file)
        else:
            self._user_dbs[db_file.user] = [db_file]

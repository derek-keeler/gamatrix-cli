"""gogdb: module that implements the RawDB contract for GOG DBs."""

from datetime import datetime
from sqlite3 import Connection
from typing import Any, Optional

from gamatrixcli.gamatrixlib.rawdb import RawDB


class GOG_DB(RawDB):
    """The GOG DB class."""

    def __init__(
        self, db_path: str, db: Connection, timestamp: datetime, username: str
    ):
        """Initialize an instance of the GOG_DB class."""
        super().__init__()
        self._user = username
        self._gog_user = ""
        self._timestamp = timestamp
        self._db = db
        self._db_path = db_path

    @property
    def db_path(self) -> str:
        return self._db_path

    @property
    def user(self) -> str:
        return self._user

    @property
    def gog_user(self) -> str:
        """The user name associated with the GOG DB specifically."""
        if self._gog_user == "":
            user_query = self.cursor.execute("select * from Users")
            if user_query.rowcount == 0:
                raise ValueError("No users found in the Users table in the DB")

            self._gog_user = self.cursor.fetchall()[0]

            if user_query.rowcount > 1:
                print(
                    "WARNING: "
                    f"Found multiple users in the DB; using the first one {self._gog_user}."
                )

        return self._gog_user

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def get_property(self, name: str, def_val: Optional[Any] = None) -> Any:
        """Return various values we require from GOGDBs, or the default value."""

        if name == "user":
            return self._user
        elif name == "gog_user":
            return self._gog_user
        elif name == "timestamp":
            return self._timestamp
        elif name == "db_path":
            return self._db_path

        # drop-through to the default value sent in.
        return def_val

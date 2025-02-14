"""gamatrixcli.config: module to track configuration for the app."""

from datetime import datetime, timezone
from pathlib import Path
import shutil
import sqlite3
from typing import Any, Dict, List, Optional

import gamatrixcli.constants as const
from gamatrixcli.gamatrixlib.config import GMConfig
from gamatrixcli.gamatrixlib.datastore import GamatrixDataStore
from gamatrixcli.gamatrixlib.rawdb import RawDB
from gamatrixcli.gamatrixlib.impl.gogdb import GOG_DB


# The default configuration file contents
DEFAULT_CONFIG: Dict[str, Any] = {
    "gamatrixcli_rc_dir": const.DEFAULT_DATASTORE_PATH.absolute(),
    "config_location": const.DEFAULT_CONFIG_PATH.absolute(),
    "db_location": const.DEFAULT_DB_PATH.absolute(),
    "user_db_location": const.DEFAULT_USER_DB_PATH.absolute(),
}


class GMCLIConfig:
    """The main configuration class for gamatrixcli."""

    def __init__(self, config: Dict[str, Any]):
        self._config_data = config
        self._user_dbs: Optional[List[RawDB]] = None
        self._gmtx_config: Optional[GMConfig] = None

    def get_property(self, name: str, def_val: Any) -> Any:
        """Get a named property from the configuration."""
        if name in self._config_data:
            return self._config_data[name]

        # fall-through to default value
        return def_val

    def get_default_config(self) -> Dict[str, Any]:
        """Return the default config in a JSON-friendly dictionary."""
        return DEFAULT_CONFIG

    def update_property(self, name: str, value: Any) -> None:
        """Update a named property in the configuration, only if the name already exists."""

        if name in self._config_data:
            self._config_data[name] = value
        else:
            raise ValueError(
                f"Property '{name}' not found in the configuration to set."
            )

    def add_db(self, user_db_file: Path, user: str) -> None:
        """Add a new DB for a new user, or an updated DB for an existing user."""
        # copy the file to the user_db folder
        userdb_path: Path = self.get_property(
            name="user_db_location", def_val=const.DEFAULT_USER_DB_PATH
        )
        stored_userdb_file = Path(userdb_path).joinpath(user_db_file.name)
        shutil.copy(src=user_db_file, dst=stored_userdb_file)  # For Python 3.8+.

        new_gogdb = GOG_DB(
            db_path=stored_userdb_file,
            db=sqlite3.connect(stored_userdb_file),
            timestamp=datetime.now(tz=timezone.utc),
        )

        self.gamatrix_datastore.add_db(db_file=new_gogdb)

    @property
    def user_dbs(self) -> List[RawDB]:
        if self._user_dbs is None:
            self._user_dbs = []
            user_db_dir: Path = self.get_property(
                name="user_db_location", def_val=const.DEFAULT_USER_DB_PATH
            )
            for db_file in user_db_dir.iterdir():
                db_conn = sqlite3.connect(database=db_file)
                db_timestamp = datetime.fromtimestamp(
                    db_file.stat().st_mtime, tz=timezone.utc
                )
                self._user_dbs.append(
                    GOG_DB(db_path=db_file.name, db=db_conn, timestamp=db_timestamp)
                )

        return self._user_dbs

    @property
    def gamatrix_config(self) -> GMConfig:
        if self._gmtx_config is None:
            self._gmtx_config = GMConfig()

        return self._gmtx_config

    @property
    def gamatrix_db(self) -> sqlite3.Connection:
        if self._gmtx_db is None:
            db_file: Path = self.get_property(
                name="db_location", def_val=const.DEFAULT_DB_PATH
            )
            self._gmtx_db = sqlite3.connect(database=db_file)

        return self._gmtx_db

    @property
    def gamatrix_datastore(self) -> GamatrixDataStore:
        if self._gmtx_datastore is None:
            self._gmtx_datastore = GamatrixDataStore(
                user_dbs=self.user_dbs, config=self.gamatrix_config, db=self.gmatrix_db
            )
        return self._gmtx_datastore

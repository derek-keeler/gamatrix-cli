"""gamatrixlib.rawdb: Handles the 'raw' user DBs.

The 'raw' user DBs are the base for all the data that gamatrixcli uses
to perform comparisons between users. These DBs are only intended to be
read upon initial ingestion (gamatrixcli's 'add-db' or gamatrix's upload-db
functionality).

The DBs are the SQLite databases that are managed by GOG, which can change
over time. Therefore the purpose of this rawdb module is also to shield the
user applications (gamatrix/gamatrixcli) from any variations in the GOG
DB format/table layout, and to provide a 'contract' should we decide to
add/replace the GOG DBs with some other source.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class RawDB:
    """The base class for the raw user DBs."""

    @property
    def db_path(self) -> str:
        """The path to the DB file."""
        raise NotImplementedError

    @property
    def user(self) -> str:
        """The user name associated with the DB."""
        raise NotImplementedError

    @property
    def timestamp(self) -> datetime:
        raise NotImplementedError

    def get_property(self, name: str, def_val: Any) -> Any:
        """Get a named property from the DB metadata or from its tables."""
        raise NotImplementedError

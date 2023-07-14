from abc import ABC, abstractclassmethod
from typing import Any, Dict, List, Optional

import psycopg2

from .data_template import DBServerInfo


class Database(ABC):
    @abstractclassmethod
    def read(self):
        pass


class Postgresql(Database):
    def __init__(self, db_server_info: DBServerInfo) -> None:
        self._db_server_info = db_server_info

    def _get_connection(self) -> psycopg2.extensions.connection:
        return psycopg2.connect(
            host=self._db_server_info.host,
            port=self._db_server_info.port,
            database=self._db_server_info.database,
            user=self._db_server_info.username,
            password=self._db_server_info.password,
        )

    def read(
        self, table_name: str, column_names: List[str], condiction: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        cur = conn.cursor()
        if condiction is None:
            cur.execute(
                "SELECT {column_names} FROM {table_name};".format(
                    column_names=",".join(column_names), table_name=table_name
                )
            )
        else:
            cur.execute(
                "SELECT {column_names} FROM {table_name} {condiction};".format(
                    column_names=",".join(column_names),
                    table_name=table_name,
                    condiction=condiction,
                )
            )
        res = []
        rows = cur.fetchall()
        for row in rows:
            row_dict = {}
            for i in range(len(row)):
                row_dict[column_names[i]] = row[i]
        cur.close()
        conn.close()
        return res

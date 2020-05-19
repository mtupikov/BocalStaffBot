import sqlite3

from tig.tig import Tig
from tig.tig_db_sql_queries import *
from datetime import datetime


class TigDatabase:
    def __init__(self):
        self._db_instance = sqlite3.connect(tig_db_name)
        cursor = self._db_instance.cursor()
        cursor.execute(create_tig_table_query)
        cursor.connection.commit()
        cursor.close()

    @staticmethod
    def convert_raw_tig_list(raw_tig_list: list) -> list:
        tig_list = []
        for username, user_id, reason, prev_tig_date, current_tig_date, is_active in raw_tig_list:
            tig = Tig(
                username,
                user_id,
                reason,
                datetime.fromisoformat(prev_tig_date),
                datetime.fromisoformat(current_tig_date),
                is_active
            )
            tig_list.append(tig)
        return tig_list

    def tig_list_by_user_id(self, user_id: int) -> list:
        cursor = self._db_instance.cursor()
        select_tuple: tuple = (user_id,)
        cursor.execute(select_active_tig_list, select_tuple)
        raw_tig_list = cursor.fetchall()
        cursor.close()
        tig_list = TigDatabase.convert_raw_tig_list(raw_tig_list)
        return tig_list

    def contains_tig_with_user_id(self, user_id: int):
        tig_list = self.tig_list_by_user_id(user_id)
        return len(tig_list) != 0

    def add_tig(self, tig: Tig):
        cursor = self._db_instance.cursor()
        cursor.execute(insert_tig_query, (
            tig.username,
            tig.user_id,
            tig.reason,
            str(tig.previous_tig_date),
            str(tig.current_tig_date),
            tig.is_active
        ))
        cursor.connection.commit()
        cursor.close()

    def set_tig_inactive(self, tig: Tig):
        tig_list = self.tig_list_by_user_id(tig.user_id)
        cursor = self._db_instance.cursor()
        if len(tig_list) >= 1:
            assert len(tig_list) == 1
            if tig_list[0].is_active:
                select_tuple: tuple = (tig.user_id,)
                cursor.execute(update_inactive_query, select_tuple)
        cursor.connection.commit()
        cursor.close()

    def update_tig(self, tig: Tig):
        cursor = self._db_instance.cursor()
        upd_tuple = (tig.reason, str(tig.previous_tig_date), str(tig.current_tig_date), tig.user_id)
        cursor.execute(update_user_tig_query, upd_tuple)
        cursor.connection.commit()
        cursor.close()

    def get_tig_list(self):
        cursor = self._db_instance.cursor()
        cursor.execute(select_all_tig_list)
        raw_tig_list = cursor.fetchall()
        cursor.close()
        return TigDatabase.convert_raw_tig_list(raw_tig_list)

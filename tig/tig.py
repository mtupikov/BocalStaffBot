from datetime import datetime, timezone, timedelta


class Tig:
    def __init__(
        self,
        username: str,
        user_id: int,
        reason: str,
        prev_tig_date: datetime,
        current_tig_date: datetime,
        is_active: bool
    ):
        self._username = username
        self._user_id = user_id
        self.reason = reason
        self.previous_tig_date = prev_tig_date
        self.current_tig_date = current_tig_date
        self.is_active = is_active

    @staticmethod
    def get_current_plus_hours(hours: int):
        return datetime.now(timezone.utc) + timedelta(hours=hours)

    @property
    def reason(self) -> str:
        return self._reason

    @reason.setter
    def reason(self, reason: str):
        self._reason = reason

    @property
    def is_active(self) -> bool:
        return self._is_active

    @is_active.setter
    def is_active(self, is_active: bool):
        self._is_active = is_active

    @property
    def username(self) -> str:
        return self._username

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def previous_tig_date(self) -> datetime:
        return self._previous_tig_date

    @previous_tig_date.setter
    def previous_tig_date(self, date: datetime):
        self._previous_tig_date = date

    @property
    def current_tig_date(self) -> datetime:
        return self._current_tig_date

    @current_tig_date.setter
    def current_tig_date(self, date: datetime):
        self._current_tig_date = date

    def formatted_current_tig_date(self) -> str:
        return self._current_tig_date.astimezone().replace(microsecond=0, tzinfo=None).isoformat()

    def formatted_previous_tig_date(self) -> str:
        return self._previous_tig_date.astimezone().replace(microsecond=0, tzinfo=None).isoformat()

    def set_up_to_date(self, new_reason: str):
        self.reason = new_reason
        new_tig_date = datetime.now(timezone.utc)
        self.previous_tig_date = self._current_tig_date
        self.current_tig_date = new_tig_date

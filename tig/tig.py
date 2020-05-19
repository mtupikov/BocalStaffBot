from datetime import datetime, timezone, timedelta


class Tig:
    def __init__(
        self,
        username: str,
        user_id: int,
        reason: str,
        current_tig_date: datetime,
        is_active: bool
    ):
        self._username = username
        self._user_id = user_id
        self.reason = reason
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
    def current_tig_date(self) -> datetime:
        return self._current_tig_date

    @current_tig_date.setter
    def current_tig_date(self, date: datetime):
        self._current_tig_date = date

    def formatted_current_tig_date(self) -> str:
        return self._current_tig_date.astimezone().replace(microsecond=0, tzinfo=None).isoformat()

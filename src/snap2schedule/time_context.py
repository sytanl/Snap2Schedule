from datetime import datetime
from zoneinfo import ZoneInfo

weekday_to_name = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}

class TimeContext:
    def __init__(
        self,
        timezone_name: str = "Asia/Ho_Chi_Minh",
        fixed_datetime: datetime | None = None,
    ):
        self.timezone_name = timezone_name
        self.timezone = ZoneInfo(timezone_name)

        if fixed_datetime is not None:
            if fixed_datetime.tzinfo is None:
                raise ValueError(
                    "fixed_datetime must be timezone-aware"
                )

            self.now = fixed_datetime.astimezone(self.timezone)
        else:
            self.now = datetime.now(self.timezone)

        self.today = self.now.date()
        self.weekday_name = weekday_to_name[self.now.weekday()]  

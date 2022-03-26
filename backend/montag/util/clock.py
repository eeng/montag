from datetime import datetime


class Clock:
    def current_timestamp(self) -> int:
        return int(datetime.timestamp(datetime.now()))

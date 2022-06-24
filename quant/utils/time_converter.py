"""
Time converter utility module
"""

from datetime import datetime, timezone
import pytz

from quant.data.config import Interval


class TimeConverter:
    """
    Time converter class
    """

    ms_per_second = 1000
    seconds_per_unit = {"m": 60, "h": 60 * 60, "d": 24 * 60 * 60, "w": 7 * 24 * 60 * 60}

    @staticmethod
    def ms_to_datetime(milis):
        """
        Convert ms to datetime
        """
        return datetime.fromtimestamp(
            milis / TimeConverter.ms_per_second, tz=timezone.utc
        )

    @classmethod
    def interval_to_ms(cls, interval: Interval):
        """
        Convert an interval to ms
        """
        value = int(interval.value[:-1])
        unit = interval.value[-1]
        unit_ms = cls.seconds_per_unit.get(unit) * cls.ms_per_second
        return value * unit_ms

    @staticmethod
    def datetime_to_ms(time: datetime):
        """
        Convert datetime to ms
        """
        if not time:
            return None

        epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
        if time.tzinfo is None or time.tzinfo.utcoffset(time) is None:
            time = time.replace(tzinfo=pytz.utc)

        return int((time - epoch).total_seconds() * TimeConverter.ms_per_second)

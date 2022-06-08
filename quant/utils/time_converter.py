from datetime import datetime, timezone
import pytz

from quant.data.config import Interval


class TimeConverter:
    ms_per_second = 1000
    seconds_per_unit = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60
    }

    @staticmethod
    def ms_to_datetime(ms):
        return datetime.fromtimestamp(ms / TimeConverter.ms_per_second, tz=timezone.utc)

    @classmethod
    def interval_to_ms(cls, interval: Interval):
        value = int(interval.value[:-1])
        unit = interval.value[-1]
        unit_ms = cls.seconds_per_unit.get(unit) * cls.ms_per_second
        return value * unit_ms

    @staticmethod
    def datetime_to_ms(t: datetime):
        if not t:
            return None

        epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
        if t.tzinfo is None or t.tzinfo.utcoffset(t) is None:
            t = t.replace(tzinfo=pytz.utc)

        return int((t - epoch).total_seconds() * TimeConverter.ms_per_second)
from datetime import datetime, timedelta

import pandas as pd

MAP_WEEKDAY_STR_TO_INT = {
    "MO": 0,
    "TU": 1,
    "WE": 2,
    "TH": 3,
    "FR": 4,
    "SA": 5,
    "SU": 6,
}


def datetime_to_date(date: datetime, hour: bool = True) -> datetime:
    """Returns a datetime object with the time set to HH:00:00."""
    if hour:
        return date.replace(minute=0, second=0, microsecond=0)
    else:
        return date.replace(hour=0, minute=0, second=0, microsecond=0)


def get_dates_from_freq(
    freq_string: str, end_date: datetime, start_date: datetime = datetime.now()
) -> pd.DatetimeIndex:
    """Returns a list of dates based on frequency."""
    start_date = datetime_to_date(start_date)
    end_date = datetime_to_date(end_date)

    if freq_string == "HOURLY":
        start_hour_date = start_date
        end_hour_date = end_date
        dates = pd.date_range(
            start=start_hour_date, end=end_hour_date, freq="H"
        )
        return dates

    start_date = datetime_to_date(start_date, hour=False)
    end_date = datetime_to_date(end_date, hour=False)

    if freq_string == "DAILY":
        start_day_date = start_date
        end_day_date = end_date
        dates = pd.date_range(start=start_day_date, end=end_day_date, freq="D")
        return dates

    if freq_string == "WEEKLY":
        start_week_date = start_date - timedelta(days=start_date.weekday())
        end_week_date = end_date - timedelta(days=end_date.weekday())
        dates = pd.date_range(
            start=start_week_date, end=end_week_date, freq="W"
        )
        return dates

    if freq_string == "MONTHLY":
        start_month_date = start_date.replace(day=1)
        end_month_date = end_date.replace(day=1, month=end_date.month)
        dates = pd.date_range(
            start=start_month_date, end=end_month_date, freq="M"
        )
        return dates

    raise ValueError("Unsupported frequency")


def get_dates_from_rrule(
    rrule: str, end_date: datetime, start_date: datetime = datetime.now()
) -> pd.DatetimeIndex:
    try:
        rrule_dict = {
            i: j for i, j in map(lambda x: x.split("="), rrule.split(";"))
        }
    except ValueError:
        raise ValueError("Invalid rrule string")

    try:
        freq_string = rrule_dict["FREQ"]
    except KeyError:
        raise ValueError("FREQ is required")

    if freq_string == "HOURLY":
        return get_dates_from_freq(freq_string, end_date, start_date)

    if freq_string == "DAILY":
        by_hour_string = rrule_dict.get("BYHOUR", "")
        if by_hour_string == "":
            return get_dates_from_freq(freq_string, end_date, start_date)
        else:
            by_hour_list = [int(i) for i in by_hour_string.split(",")]

            if not all(0 <= i <= 23 for i in by_hour_list):
                raise ValueError("BYHOUR values must be between 0 and 23")

            dates = get_dates_from_freq("HOURLY", end_date, start_date)
            dates = dates[dates.hour.isin(by_hour_list)]
            return dates

    if freq_string == "WEEKLY":
        by_day_string = rrule_dict.get("BYDAY", "")
        if by_day_string == "":
            return get_dates_from_freq(freq_string, end_date, start_date)
        else:
            try:
                by_day_list = [
                    MAP_WEEKDAY_STR_TO_INT[i.upper()]
                    for i in by_day_string.split(",")
                ]
            except KeyError:
                raise ValueError("Invalid weekday in BYDAY")

            dates = get_dates_from_freq("DAILY", end_date, start_date)
            return dates[dates.weekday.isin(by_day_list)]

    if freq_string == "MONTHLY":
        by_monthday_string = rrule_dict.get("BYMONTHDAY", "")
        if by_monthday_string == "":
            return get_dates_from_freq(freq_string, end_date, start_date)
        else:
            by_monthday_list = [int(i) for i in by_monthday_string.split(",")]
            if not all(1 <= i <= 31 for i in by_monthday_list):
                raise ValueError("BYMONTHDAY values must be between 1 and 31")

            dates = get_dates_from_freq("DAILY", end_date, start_date)
            return dates[dates.day.isin(by_monthday_list)]

    raise ValueError("Unsupported frequency")

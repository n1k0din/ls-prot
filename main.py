from collections import namedtuple
from datetime import datetime, timedelta
import typing as t

Point = namedtuple("Point", ["t", "f"])

ROUND_TO_HOUR = {
    "microsecond": 0,
    "second": 0,
    "minute": 0
}

ONE_HOUR = timedelta(hours=1)


def td_minutes(td: timedelta) -> float:
    return td.seconds / 60


def approx(p1: Point, p2: Point, max_segment=120) -> t.List[Point]:
    """
    на входе данные за 7:24 и 8:15
    на выходе линейно приближенное значение в 8:00
    """
    delta = p2.t - p1.t
    delta_minutes = td_minutes(delta)

    if delta_minutes >= max_segment:
        return None

    k = (p2.f - p1.f) / delta_minutes

    i = (p1.t + ONE_HOUR).replace(**ROUND_TO_HOUR)

    res = []

    while i <= p2.t:
        p0 = Point(i, k * td_minutes(i - p1.t) + p1.f)
        res.append(p0)
        i += ONE_HOUR


    return res


def main():
    p1 = Point(datetime(2020, 9, 1, 7, 24), 4)
    p2 = Point(datetime(2020, 9, 1, 9, 15), 14)
    print(approx(p1, p2, max_segment=120))


if __name__ == "__main__":
    main()
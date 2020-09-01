from collections import namedtuple
from datetime import datetime, timedelta

Point = namedtuple("Point", ["t", "f"])


def td_minutes(td: timedelta) -> float:
    return td.seconds / 60


def approx(p1: Point, p2: Point) -> Point:
    """
    на входе данные за 7:24 и 8:15
    на выходе линейно приближенное значение в 8:00
    """
    delta = p2.t - p1.t
    delta_minutes = td_minutes(delta)

    if delta_minutes >= 60:
        return None

    k = (p2.f - p1.f) / delta_minutes

    t0 = p2.t.replace(second=0, microsecond=0, minute=0)

    res = k * td_minutes(t0 - p1.t) + p1.f

    return res


def main():
    p1 = Point(datetime(2020, 9, 1, 7, 24), 4)
    p2 = Point(datetime(2020, 9, 1, 8, 15), 14)
    print(approx(p1, p2))


if __name__ == "__main__":
    main()
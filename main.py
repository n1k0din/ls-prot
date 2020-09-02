from collections import namedtuple
from datetime import datetime, timedelta
import typing as t
import csv


Point = namedtuple("Point", ["t", "f"])

ROUND_TO_HOUR = {
    "microsecond": 0,
    "second": 0,
    "minute": 0
}

ONE_HOUR = timedelta(hours=1)

# 21.01.2020 12:02
DAY = slice(0, 2)
MONTH = slice(3, 5)
YEAR = slice(6, 10)
HOURS = slice(11, 13)
MINUTES = slice(14, 16)
SECONDS = slice(17, 19)


def str_to_datetime(string: str) -> datetime:
    try:
        year = int(string[YEAR])
        month = int(string[MONTH])
        day = int(string[DAY])
        hours = int(string[HOURS])
        minutes = int(string[MINUTES])
        seconds = int(string[SECONDS])

        return datetime(year, month, day, hours, minutes, seconds)
    except ValueError:
        raise ValueError(string)


def csvfile_to_list(filename: str, dialect='excel'):
    """
    читает csv файл с определенным диалектом в список, игнорирует первую строку
    """
    raw_data = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, dialect=dialect)
        _ = reader.__next__()
        for row in reader:
            raw_data.append(row)
        return raw_data


def strings_to_points(strlist) -> t.List[Point]:

    points = []

    for dt, num in strlist:
        dt = str_to_datetime(dt)
        num = int(num)

        points.append(Point(dt, num))

    return points


def approx_points_list(points):
    n = len(points)
    print("n = ", n)
    res = []
    print(approx(points[0], points[1]))

    for i in range(1, n):
        res.extend(approx(points[i - 1], points[i]))

    return res


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


def print_points(points):
    for point in points:
        print(point.t, point.f, sep=';')


def main():

    csv.register_dialect('winwin', delimiter=';')

    raw_data = csvfile_to_list("approx-input.csv", dialect='winwin')

    points = strings_to_points(raw_data)

    approx_points = approx_points_list(points)

    print_points(approx_points)




if __name__ == "__main__":
    main()
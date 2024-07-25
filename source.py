import time


def custom_1():
    time.wait(10)


tasks_list = [
    (custom_1, ()),
    (min, (3, 7, 44, 2)),
    (max, (3, 7, 44, 2)),
    (len, (4, 5, 6, 6)),
    (sum, (-100, 300)),
]

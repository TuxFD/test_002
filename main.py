import time
from controller import ProcessController


def custom_1(a, b, c, queueu):
    time.sleep(0.5)
    queueu.put("custom_1 returned ")


def custom_2(a, b, queueu):
    time.sleep(1.5)
    queueu.put("custom_2 returned ")


def custom_3(a, queueu):
    time.sleep(3)
    queueu.put("custom_3 returned ")


def custom_4(queueu):
    time.sleep(5)
    queueu.put("custom_4 returned ")


def custom_5(a, b, queueu):
    time.sleep(100)
    queueu.put("custom_5 returned ")


tasks_list = [
    (custom_1, [2, 2, 2]),
    (custom_2, [2, 2]),
    (custom_3, [2]),
    (custom_4, []),
    (custom_5, [2, 2]),
]


# ========
def main():
    pc = ProcessController()
    pc.set_max_proc(2)
    pc.start(tasks_list, max_exec_time=4)


if __name__ == "__main__":
    main()

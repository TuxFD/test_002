from source import tasks_list
from controller import ProcessController


# ========
def main():
    pc = ProcessController()
    pc.set_max_proc(3)
    pc.start(tasks_list, max_exec_time=1)


if __name__ == "__main__":
    main()

import time
from multiprocessing import Process, Queue


class ProcessController:
    def __init__(self) -> None:
        self.all_tasks = Queue()
        self.run_tasks = Queue()
        self.done_tasks = Queue()
        self.proc = []
        self.proc_timer = {}
        self.proc_timeout = int(0)
        self.limit = 0

    # def wait(self):
    #     return self.run_tasks.qsize()

    def wait_count(self):
        return self.all_tasks.qsize()

    def alive_count(self):
        return self.run_tasks.qsize()

    def set_max_proc(self, n):
        num = int(n)
        if num > 0:
            self.limit = n
        else:
            print("Invalid processes number")
            exit(1)

    def start(self, tasks: list, max_exec_time: float):
        try:
            # ==== [1] ==== Create all_tasks Queue
            for task in tasks:
                self.all_tasks.put(task)
            print(f"QUEUE CREATED. SIZE: {self.all_tasks.qsize()}")
            print("QUEUE ELEMENTs:")
            for i in range(self.all_tasks.qsize()):
                elem = self.all_tasks.get()
                print(elem)
                self.all_tasks.put(elem)
            print()

            # ==== [2] ==== Create loop to empty all_tasks Queue
            while self.wait_count() > 0:

                # ==== [3] ==== Create limited run_tasks Queue
                while (
                    not self.all_tasks.empty() and self.run_tasks.qsize() < self.limit
                ):
                    my_task = self.all_tasks.get()
                    self.run_tasks.put(my_task)
                else:
                    print()
                    print(f"LIMITED QUEUE CREATED. SIZE: {self.run_tasks.qsize()}")
                    print("LIMITED QUEUE ELEMENTs:")
                    for i in range(self.run_tasks.qsize()):
                        elem = self.run_tasks.get()
                        print(elem)
                        self.run_tasks.put(elem)
                    print()

                # ==== [3] ==== Spawn processes
                while self.alive_count() > 0:
                    try:
                        runtask = self.run_tasks.get()
                        print(
                            "TASK IN PROCESS:",
                            runtask,
                            "ALIVE COUNT: ",
                            self.alive_count(),
                        )
                        try:
                            runtask[1].append(self.done_tasks)
                            p = Process(
                                target=runtask[0],
                                args=runtask[1],
                            )
                            p.start()
                            p_start = time.time()
                            self.proc.append(p)
                            self.proc_timer[p.name] = p_start
                            # ==== [4] ==== Wait for limited queue tasks to finish
                            for p in self.proc:
                                p.join(max_exec_time)  # TIMEOUT

                                # ==== [5] ==== Processes terminator
                                while p.is_alive():
                                    p_started = self.proc_timer[p.name]
                                    if time.time() - p_started - 1 < max_exec_time:
                                        p.terminate()
                                        self.proc_timedout += 1

                        except Exception as e:
                            print()
                            print("==== ERROR ====: ", e)

                    except Exception as e:
                        print()
                        print("==== ERROR ====: ", e)

                else:
                    print("DONE!")
                    print("")

            else:
                print("QUEUE EMPTY! RESULTs:")
                while not self.done_tasks.empty():
                    print(self.done_tasks.get())
                print("PROCESSES TIMED OUT:", self.proc_timedout)

        except Exception as e:
            print()
            print("==== ERROR ====: ", e)

# import time
import queue
from multiprocessing import Process, Queue

# additional data
from source import tasks_list


class ProcessController:
    def __init__(self) -> None:
        self.all_tasks = Queue()
        self.run_tasks = Queue()
        self.timeout_tasks = Queue()
        self.done_tasks = Queue()
        self.proc = []
        self.limit = 0

    def wait(self):
        return self.run_tasks.qsize()

    def wait_count(self):
        return self.all_tasks.qsize()
    
    def alive_count(self):
        return self.run_tasks.qsize()

    def set_max_proc(self, n: int):
        self.limit = n

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
                while not self.all_tasks.empty() and self.run_tasks.qsize() < self.limit:
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
                        print('TASK IN PROCESS:', runtask, 'ALIVE COUNT: ', self.alive_count())
                        # try:
                        #     p = Process(target=runtask[0], args=runtask[1])
                        #     self.proc.append(p)
                        #     p.start()
                        # except Exception as e:
                        #     print("==== ERROR ====: ", e)

                    except Exception as e:
                        print()
                        print("==== ERROR ====: ", e)
                
                else:
                    print('DONE!')

                    # ==== [4] ==== Wait for limited queue tasks to finish
                    # for p in self.proc:
                    #     p.join(max_exec_time)  # TIMEOUT

            else:
                print("QUEUE EMPTY!")

        except Exception as e:
            print("==== ERROR ====: ", e)


# ======== TODO: delete this later
def main():
    pc = ProcessController()
    pc.set_max_proc(3)
    pc.start(tasks_list, max_exec_time=1)


if __name__ == "__main__":
    main()

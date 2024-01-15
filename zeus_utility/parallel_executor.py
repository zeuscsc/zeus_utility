from typing import Callable, Iterator
import time
HEADLESS=True

class Queue:
    executing_function:Callable=None
    kawrgs:dict=None

class QueueExecutor(list[Queue]):
    def __init__(self,threads_count:int=5,slience=True,waiting_time=0):
        super().__init__()
        self.threads_count=threads_count
        self.slience=slience
        self.waiting_time=waiting_time
        pass
    def add_task(self,task:Callable,**kwargs):
        super().append((task,kwargs))

    def execute(self):
        execute_queue(self,threads_count=self.threads_count,slience=self.slience,waiting_time=self.waiting_time)
    pass
def execute_queue(iterator:Iterator,threads_count:int=10,slience=True,waiting_time=0):
    def run_task(task:Callable,*args, **kwargs):
        # try:
            task(*args, **kwargs)
        # except Exception as e:
        #     print(e)
    from queue import Queue
    from threading import Thread
    WORKERS_COUNT=threads_count
    queue = Queue()
    def worker():
        continue_running=True
        while continue_running:
            try:
                row=queue.get()
                task=None
                if isinstance(row,tuple) or isinstance(row,list):
                    task=row[0]
                    parameters=row[1]
                if isinstance(row,dict):
                    if "task" in row:task=row["task"]
                    if "function" in row:task=row["function"]
                    if "func" in row:task=row["func"]
                    if "parameter" in row:parameters=row["parameter"]
                    if "parameters" in row:parameters=row["parameters"]
                    if "params" in row:parameters=row["params"]
                    if "args" in row:parameters=row["args"]

                if isinstance(parameters,tuple) or isinstance(parameters,list):
                    args=parameters
                    kwargs={}
                elif isinstance(parameters,dict):
                    args=[]
                    kwargs=parameters
                if not slience:
                    print(f"Running {args}")
                run_task(task,*args, **kwargs)
                if not slience:
                    print(f"Task done.")
                queue.task_done()
            except KeyboardInterrupt:
                print("Main process terminated externally.")
                break
            except BaseException as e:
                continue_running=False
                raise e
    for i in range(WORKERS_COUNT):
        Thread(target=worker, daemon=True).start()
    def start():
        for row in iterator:
            queue.put(row)
            time.sleep(waiting_time)
        queue.join()
    return start()

import multiprocessing
from multiprocessing import Queue, Lock
import time
from data_stream import start_process_data
from stream1 import start_stream_1
from stream2limit import start_stream_2
from stream3 import start_stream_3

if __name__ == '__main__':

    queue = Queue(maxsize=10)
    # queue2 = Queue(maxsize=2)
    # queue3 = Queue(maxsize=2)
    # lock = Lock()
    # shared_dict = {}

    process1 = multiprocessing.Process(target=start_process_data, args=(queue,))
    process1.start()


    process2 = multiprocessing.Process(target=start_stream_1, args=(queue,))
    process2.start()

    process3 = multiprocessing.Process(target=start_stream_2, args=(queue,))
    process3.start()

    process4 = multiprocessing.Process(target=start_stream_3, args=(queue,))
    process4.start()



    try:
        while True:
            pass

    except KeyboardInterrupt:

        process1.terminate()
        process2.terminate()
        process3.terminate()
        process4.terminate()

        process1.join()
        process2.join()
        process3.join()
        process4.join()
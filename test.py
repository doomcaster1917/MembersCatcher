import multiprocessing as mp
from controller import TelegramApi
import time
TelegramApi = TelegramApi()
def foo_pool(x):
    time.sleep(2)
    return x*x
result_list = []
def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    print(result)
def apply_async_with_callback():
    try:
        pool = mp.Pool()
        pool.apply_async(TelegramApi.foo_pool, args = ('@elektro_velo_servis', ), callback = log_result)
        pool.close()
        pool.join()
        print(result_list)
    except Exception as err:
        print(err)
if __name__ == '__main__':
    apply_async_with_callback()
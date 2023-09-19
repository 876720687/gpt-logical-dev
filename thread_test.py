import threading
import requests
from tools import *
# 要下载的URL列表
urls = ['https://www.example.com', 'https://www.example.org', 'https://www.example.net']




# 线程函数，负责下载指定URL的内容
def download_url(url):
    response = requests.get(url)
    print(f"Downloaded {len(response.text)} bytes from {url}")


@time_calculate
def threads_process(): # python当中更推荐使用协程
    # 创建线程列表
    threads = []

    # 创建并启动线程
    for url in urls:
        thread = threading.Thread(target=download_url, args=(url,))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    return



if __name__ == "__main__":
    # 计算总时间
    # # 记录开始时间
    # start_time = time.time()

    threads_process()

    # end_time = time.time()
    # total_time = end_time - start_time
    # print(f"Total time taken: {total_time:.2f} seconds")

import time

# 定义时间测量装饰器
def time_calculate(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} took {elapsed_time:.2f} seconds to run.")
        return result
    return wrapper





# =====================================测试修饰器=============================================

# 使用装饰器来测量函数的执行时间
@time_calculate
def example_function():
    # 这里可以是需要测量执行时间的函数代码
    time.sleep(2)

if __name__ == "__main__":
    example_function()

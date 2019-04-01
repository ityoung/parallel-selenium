"""
将一个用例拓展为多个进程，在多个浏览器上并发执行

@author: Shin
@date: 2019-04-01
"""
import functools
import unittest
import multiprocessing
import traceback


class Process(multiprocessing.Process):
    """
    为multiprocessing.Process添加子进程错误抛出功能，并且获取浏览器信息输出在错误栈中。
    """

    def __init__(self, *args, **kwargs):
        super(Process, self).__init__(*args, **kwargs)

        self._pconn, self._cconn = multiprocessing.Pipe()
        self._exception = None
        self._driver = self.extract_driver_info(**kwargs)

    def run(self):
        try:
            super(Process, self).run()
            self._cconn.send(None)
        except AttributeError as e:
            tb = traceback.format_exc()
            e = Exception(f'{tb}BrowserInfomation: {self._driver}')
            self._cconn.send((e, self._driver))
        except Exception as e:
            tb = traceback.format_exc()
            e.msg = f'{tb}\nBrowserInfomation: {self._driver}'
            self._cconn.send((e, self._driver))

    def extract_driver_info(self, **kwargs) -> dict:
        """
        从传入的参数中获取浏览器信息
        :param kwargs: 
        :return: 
        """
        args = kwargs.get('args', None)
        if args is None:
            return {}
        driver = args[1].desired_capabilities
        light_driver_info = dict(
            browserName=driver['browserName'],
            # TODO: Version
        )
        return light_driver_info

    @property
    def exception(self) -> None or tuple:
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return self._exception


def multiply(func):
    """
    测试用例装饰器，使得每个用例在不同浏览器执行多次
    :param test: 
    :return: 
    """

    class SingleTestCase(unittest.TestCase):
        def __init__(self, driver):
            super().__init__()
            # 由于此处限定了类属性名为driver, 在调用WebDriver对象的时候需要与此处一致。
            # 例如： self.driver.find_element_by_id()
            self.driver = driver

    def thread_func(f, driver=None):
        f(SingleTestCase(driver))

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 由于此处限定了类属性名为drivers, 在初始化WebDriver时需要保持一致
        # 例如： self.drivers = [WebDriver.Remote(), WebDriver.Remote()]
        drivers = args[0].drivers
        process = []

        for i in drivers:
            p = Process(target=thread_func, args=(func, i))
            p.start()
            process.append(p)

        for p in process:
            p.join()

        for p in process:
            if p.exception:
                e, d = p.exception
                raise e

    return wrapper

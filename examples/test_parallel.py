"""
测试用例示例

@author: Shin
@date: 2019-04-01
"""
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from libs import parallel


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # 此处假设你在本机启动了一个Selenium Grid, 且有Chrome与IE的Node节点
        self.drivers = [
            webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME
            ),
            webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.INTERNETEXPLORER
            )
        ]

    @parallel.multiply
    def tearDown(self):
        self.driver.quit()

    @parallel.multiply
    def test_parallel(self):
        # 注意，此处变量名为`driver`，非`setUp`方法中的`drivers`
        self.driver.get('https://intest.tech')
        time.sleep(5)

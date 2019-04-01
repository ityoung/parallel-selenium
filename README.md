# parallel-selenium
使用Python并发地在不同浏览器上同时运行Selenium测试用例.

主要代码借鉴了*参考*中的两份代码，在这之上做了一些优化，使得子进程中执行用例时能够失败并返回浏览器信息。

## 实现方式

将一个用例拓展为多个进程，在多个浏览器上并发执行。

在每个子进程中，显式地抛出异常给主进程捕获，使得子进程在执行失败后测试用例能够正常失败。

## 用法

### 执行示例程序

安装依赖：

```commandline
pip install -r requirements.txt
```

运行测试：

```commandline
python -m unittest discover
```

### 应用于你的项目

复制`libs.parallel.py`中的代码到你的项目中，参考示例代码(`examples.test_parallel.py`)重新组织你当前的代码。

在`setUp`方法中定义一个`self.drivers`，以list形式存储多个`WebDriver`对象。

对需要并发执行的测试用例和`tearDown`方法，使用装饰器`parallel.multiply`装饰即可。

## 参考

1. https://stackoverflow.com/questions/19924104/python-multiprocessing-handling-child-errors-in-parent
2. https://github.com/OniOni/python-parallel-wd/blob/master/wd/parallel.py

## 推荐阅读

1. [理解浏览器兼容性自动化测试过程](https://www.jianshu.com/p/91b2425af663)

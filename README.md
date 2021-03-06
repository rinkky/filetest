# filetest

文件测试框架。对资源文件属性和文件内容进行测试，并生成测试报告。

## 快速运行
将用例模块，被测文件以及日志目录配置在`config.py`中，运行`run.py`. 测试结果将打印并保存为日志文件。

## 配置

#### config.py

`collection`保存了一个列表，用来存储测试方法和被测文件，列表中每个元素形如：

```
    {
        "name":"sample1",
        "models":[
            "testcases.testfile.model1",
            "testcases.txttable.model2"
        ],
        "files":[
            r"path1/*.txt",
            r"path2/*.png"
        ]
    }
```

针对该配置，模块`model1`和`model2`中的所有用例会先对`path1`中的所有txt文件进行测试，然后对`path2`中的所有png文件进行测试。

`log_base_path`用来定义测试日志保存位置。

#### 日志

默认将日志打印到屏幕上，并将所有测试未通过的信息保存为log文件。

日志由`testlog`中的`LogThread`控制，如果需要对日志进行更多操作，可以编写自己的log线程。日志通过`log_queue`传播，log线程只需要接收并处理`log_queue`.

## 用例

一个`.py`文件可以包含一个用例集合。每个用例集合中可以包含一个`setup()`，一个`teardown()`，和多个`test_*()`. 


`test_*()`，用例文件中每一个以`test_`开头的函数都会被当成一个用例执行，可以用来进行一些初始化操作；

`setup()`，在用例集中的所有用例执行之前执行；

`teardown()`，同一用例集中的所有用例执行之后，如果存在`teardown()`，将会被执行，可以用来关闭文件或其他清理操作。

## 扩展

框架目前包含对表格内容的各项测试，如升序测试、唯一性测试、非空测试、值有效性测试、类型测试等。

可以将更多文件测试项添加到框架中，如各种美术资源测试。将测试用到的API放到`utils`中，测试用例放到`testcases`中。

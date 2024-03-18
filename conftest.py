import pytest
from _pytest.main import Session
from _pytest.nodes import Item
from pluggy import Result
import datetime
import time


start_timestr = None
end_timestr = None
durning = None
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_call(item: "Item"):
#     """查看具体的测试案例实际执行时间"""
#     global start_timestr,end_timestr,durning
#     start_timestr = datetime.datetime.now()
#     print( f"{item.name}测试用例于{start_timestr}开始执行>>>>>>>>>>>" )
#
#     outcome = yield
#     end_timestr = datetime.datetime.now()
#     print(f"{item.name}测试用例在{end_timestr}执行完毕了>>>>>>>>>>>")
#     # print(f"outcome的返回结果是{outcome}，看看")
#     durning = "".format()
#     print(f"{item.name}案例执行耗时{(end_timestr-start_timestr)}>=<")
#     outcome.force_result(0)

def pytest_configure():

    print("测试案例开始执行了")

def pytst_unconfigure():

    print("测试案例执行完毕了")

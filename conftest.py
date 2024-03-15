import pytest
from _pytest.main import Session
from _pytest.nodes import Item
from pluggy import Result


@pytest.hookimpl(hookwrapper = True)
def pytest_runtest_call(item:"Item"):
	print(f"{item.name}测试用例开始执行>>>>>>>>>>>")

	outcome = yield

	print( f"{item.name}测试用例完毕了>>>>>>>>>>>" )
	print(f"outcome的返回结果是{outcome}，看看")
	outcome.force_result(0)
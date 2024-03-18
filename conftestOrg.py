from datetime import datetime, time
from pathlib import Path
from typing import List, Optional

import pytest
import requests
from _pytest import nodes
from _pytest.config import Config
from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.python import Function, Package
from _pytest.reports import TestReport
from _pytest.skipping import Xfail
from _pytest.stash import StashKey
from wxpy import *

xfailed_key = StashKey[Optional[Xfail]]()

# def pytest_collect_directory( path: Path, parent: nodes.Collector) -> Optional[nodes.Collector]:
# 	pkginit = path / "__init__.py"
# 	if pkginit.is_file():
# 		return Package.from_parent(parent, path=path)
# 	return None

# @pytest.hookimpl(hookwrapper = True)
# def pytest_pyfunc_call(pyfuncitem:"Function"):
# 	print("这个地方会干啥+pyfuncitem：{pyfuncitem}")
#
# 	outcome = yield
# 	print(f"pyfuncitem到底时啥啥{pyfuncitem}")
# 	print( f"嗯哼{pyfuncitem.name}" )
#
# 	res = outcome.get_result()
#
# 	print(f"执行后插件会干啥{res}")


# def pytest_collection_modifyitems(session:Session,config:Config,items:List[Item]):
# 	date = {}
#
# 	for item in session.items:
# 		print(f"测试案例的名称为：{item.name}；节点ID为：{item.nodeid}；文件路径为：{item.path}")
# 		# print(f"测试案例的节点ID为：{item.nodeid}")
# 		# print(f"测试案例的文件路径为：{item.path}")
# 	date["total"] = session.testscollected
# 	date["failed"] = session.testsfailed
# 	print(f"总计收集到测试案例{len(items)}，测试案例收集完毕")
# 	sucess_rate= (date["total"]/len(items))
# 	print(f"测试成功率= {sucess_rate}")

# @pytest.hookimpl(hookwrapper = True,tryfirst = True)
# def pytest_runtest_call(item:Item):
# 	print(f"{item.name}测试用例执行开始时间{datetime.now()}")
#
# 	outcome = yield
#
# 	print(f"{item.name}测试用例执行时间是：{datetime.now()},执行结果为：{item.stash.get(xfailed_key,None)}")
# 	# if not outcome.get_result():
# 	print("开始修改失败案例为成功")
# 	outcome.force_result(0)
# @pytest.hookimpl()
# def pytest_runtest_logreport(report:TestReport):
#
# 	outcome = yield
# 	if report.outcome== "passed":
# 		print("执行成功案例+1")
# 	if report.outcome == "failed":
# 		print("执行失败案例+1")
# 	if report.outcome == "skipped":
# 		print("跳过案例+1")


import os
from datetime import datetime
from typing import List

import pytest
import requests
from _pytest.config import Config, hookspec
from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.reports import TestReport

total_cases = 0
skiped_cases = 0
passed_cases = 0
failed_cases = 0
start_times = {}
end_times = {}


def pytest_collection_modifyitems(
    session: Session, config: Config, items: List["Item"]
):
    global total_cases
    total_cases = len(items)


def pytest_runtest_setup(item: Item):
    start_times[item.nodeid] = datetime.now()


def pytest_runtest_logreport(report: TestReport):
    global skiped_cases, passed_cases, failed_cases

    if report.when == "call":
        if report.passed:
            print(f"测试的执行结果是：{report.outcome}*********")
            passed_cases += 1
        elif report.failed:
            failed_cases += 1
        elif report.skipped:
            skiped_cases += 1

        end_times[report.nodeid] = datetime.now()
        duration = (datetime.now() - start_times[report.nodeid]) * 1000
        print(
            f"\n{str(report.nodeid).split('::')[-1]}案例执行开始时间：{start_times[report.nodeid]}；结束时间{end_times[report.nodeid]}；执行耗时{duration}"
        )


def pytest_sessionfinish(session: Session):
    print(f"总计收集到案例{total_cases}条\n")
    print(f"执行成功案例{passed_cases}条\n")
    print(f"执行失败案例{failed_cases}条\n")
    success_rate = passed_cases / total_cases if total_cases > 0 else 0
    failure_rate = failed_cases / total_cases if total_cases > 0 else 0
    coverage_rate = (
        (passed_cases + failed_cases) / total_cases if total_cases > 0 else 0
    )
    print(
        f"案例执行完毕：成功率{success_rate}\n失败率{failure_rate}\n覆盖率{coverage_rate}"
    )
    success_rate = "{:.2%}".format(success_rate)
    failure_rate = "{:.2%}".format(failure_rate)
    coverage_rate = "{:.2%}".format(coverage_rate)
    # 	result_msg = f"33333333333333333333333333333总计收集到案例:{total_cases}条;执行成功案例:{passed_cases}条;执行失败案例:{failed_cases}条;案例成功率:{success_rate};案例失败率:{failure_rate};案例覆盖率:{coverage_rate}"
    # #开始发送测试结果到微信消息的文件助手
    # 	bot = Bot(cache_path= True)
    #
    # 	bot.file_helper.send(content="12345666")
    url = r"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4798277e-32d4-4cc3-8bdb-cadb579d45fc"
    json_date = {
        "msgtype": "markdown",
        "markdown": {
            "content": f"""本次测试共执行案例<font color=\"warning\">{total_cases}条</font>，请相关同事知悉！其中\n
    	     >测试通过数:<font color=\"green\">{passed_cases}</font>
    	     >测试失败数:<font color=\"red\">{failed_cases}</font>
    	     >测试通过率:<font color=\"green\">{success_rate}</font>
			 >测试失败率:<font color=\"red\">{failure_rate}</font>
			 >测试覆盖率:<font color=\"comment\">{coverage_rate}</font>
			 >测试报告地址:<font color=\"green\">https://www.baidu.com</font>"""
        },
    }
    response = requests.post(url=url, json=json_date)
    print(response.text)

from __future__ import annotations

import unittest

import pandas as pd

from core.repair_orders.quality import build_quality_issues


class StandardFaultQualityTests(unittest.TestCase):
    def test_quality_issues_flag_common_field_problems(self) -> None:
        data = pd.DataFrame(
            [
                {
                    "源表行号": "2",
                    "隧道名称": "测试隧道",
                    "故障日期": "2026-07-01",
                    "故障地点": "右洞入口",
                    "设备名称": "摄像机",
                    "设备分类": "",
                    "故障现象": "",
                    "处置措施": "",
                    "修复时间": "",
                    "原因及处理": "电源故障，电源故障",
                },
                {
                    "源表行号": "2",
                    "隧道名称": "测试隧道",
                    "故障日期": "2026-07-01",
                    "故障地点": "YK12+345",
                    "设备名称": "摄像机",
                    "设备分类": "监控与通信设施",
                    "故障现象": "图像离线",
                    "处置措施": "更换电源后恢复",
                    "修复时间": "2026-07-01 12:00:00",
                    "原因及处理": "更换电源后恢复",
                },
            ]
        )

        issue_names = {item["检查项"] for item in build_quality_issues(data)}

        self.assertIn("故障现象为空", issue_names)
        self.assertIn("处置措施为空", issue_names)
        self.assertIn("故障地点未识别到桩号", issue_names)
        self.assertIn("设备分类为空", issue_names)
        self.assertIn("同一源表行号重复", issue_names)
        self.assertIn("原因及处理疑似重复", issue_names)

    def test_same_device_same_day_different_fault_content_is_not_duplicate(self) -> None:
        data = pd.DataFrame(
            [
                {
                    "源表行号": "10",
                    "隧道名称": "永井隧道",
                    "故障日期": "2026-07-03",
                    "故障地点": "YK12+345",
                    "设备名称": "工业以太网交换机",
                    "故障现象": "通信中断",
                    "故障原因": "电源模块异常",
                    "处置措施": "更换电源模块",
                },
                {
                    "源表行号": "11",
                    "隧道名称": "永井隧道",
                    "故障日期": "2026-07-03",
                    "故障地点": "YK12+345",
                    "设备名称": "工业以太网交换机",
                    "故障现象": "端口掉线",
                    "故障原因": "光纤接头松动",
                    "处置措施": "重新熔接并固定接头",
                },
            ]
        )

        issue_names = {item["检查项"] for item in build_quality_issues(data)}

        self.assertNotIn("疑似重复故障记录", issue_names)

    def test_same_device_same_day_same_fault_content_is_duplicate(self) -> None:
        data = pd.DataFrame(
            [
                {
                    "源表行号": "20",
                    "隧道名称": "永井隧道",
                    "故障日期": "2026-07-03",
                    "故障地点": "YK12+345",
                    "设备名称": "工业以太网交换机",
                    "故障现象": "通信中断",
                    "故障原因": "电源模块异常",
                    "处置措施": "更换电源模块",
                },
                {
                    "源表行号": "21",
                    "隧道名称": "永井隧道",
                    "故障日期": "2026-07-03",
                    "故障地点": " YK12 + 345 ",
                    "设备名称": " 工业以太网交换机 ",
                    "故障现象": "通信中断",
                    "故障原因": "电源模块异常",
                    "处置措施": "更换电源模块",
                },
            ]
        )

        issues = build_quality_issues(data)
        duplicate_issues = [item for item in issues if item["检查项"] == "疑似重复故障记录"]

        self.assertEqual(1, len(duplicate_issues))
        self.assertEqual(2, duplicate_issues[0]["数量"])


if __name__ == "__main__":
    unittest.main()

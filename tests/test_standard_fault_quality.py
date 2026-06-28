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


if __name__ == "__main__":
    unittest.main()

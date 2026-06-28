from __future__ import annotations

import unittest

from core.repair_orders.report_text import build_fault_phenomenon, combine_reason_and_action, normalize_report_text


class ReportTextPolicyTests(unittest.TestCase):
    def test_fault_phenomenon_removes_repeated_tunnel_and_location(self) -> None:
        self.assertEqual(
            build_fault_phenomenon(
                tunnel_name="永新隧道",
                fault_location="YK12+345",
                description="永新隧道YK12+345紧急电话离线。",
                device_name="紧急电话",
            ),
            "紧急电话离线",
        )

    def test_fault_phenomenon_keeps_new_month_wording_without_phrase_table(self) -> None:
        self.assertEqual(
            build_fault_phenomenon(
                tunnel_name="永新隧道",
                fault_location="ZK8+100",
                description="ZK8+100摄像机夜间画面偏色，偶发闪烁",
                device_name="摄像机",
            ),
            "摄像机夜间画面偏色，偶发闪烁",
        )

    def test_fault_phenomenon_removes_leading_separator_after_location_strip(self) -> None:
        self.assertEqual(
            build_fault_phenomenon(
                tunnel_name="肖家山隧道",
                fault_location="YK389+535、YK389+793、YK390+077、YK390+297",
                description="YK389+535、YK389+793、YK390+077、YK390+297、车道指示器故障",
                device_name="工业以太网交换机",
            ),
            "车道指示器故障",
        )

    def test_reason_and_action_combination_avoids_repeated_cause(self) -> None:
        self.assertEqual(
            combine_reason_and_action("电源模块故障", "现场检查为电源模块故障，更换模块后恢复"),
            "现场检查为电源模块故障，更换模块后恢复",
        )

    def test_reason_and_action_combination_keeps_distinct_details(self) -> None:
        self.assertEqual(
            combine_reason_and_action("光纤接头松动", "重新插拔并固定接头"),
            "光纤接头松动，重新插拔并固定接头",
        )

    def test_normalize_report_text_compacts_spacing_and_terminal_punctuation(self) -> None:
        self.assertEqual(normalize_report_text("  情报板  通讯异常； "), "情报板 通讯异常")
        self.assertEqual(normalize_report_text("】【‘；/。，！车道指示器故障】【‘；/。，！"), "车道指示器故障")
        self.assertEqual(normalize_report_text(" /PLC控制器故障！ "), "PLC控制器故障")


if __name__ == "__main__":
    unittest.main()

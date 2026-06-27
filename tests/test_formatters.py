from __future__ import annotations

import unittest

from generators.monthly_reports.common import generation_progress_message
from pages.home_formatters import date_range_metric_html, format_metric_date


class HomeFormatterTests(unittest.TestCase):
    def test_format_metric_date_normalizes_datetime_text(self) -> None:
        self.assertEqual(format_metric_date("2026-06-02 12:34:56"), "2026-06-02")
        self.assertEqual(format_metric_date("2026-06-22"), "2026-06-22")

    def test_date_range_metric_html_reflects_upload_state(self) -> None:
        self.assertIn("待上传", date_range_metric_html(None, False))
        self.assertIn("已选择文件", date_range_metric_html(None, True))

    def test_date_range_metric_html_uses_parsed_dates_only(self) -> None:
        html = date_range_metric_html({"date_start": "2026-06-02", "date_end": "2026-06-22"}, True)
        self.assertIn("2026-06-02", html)
        self.assertIn("2026-06-22", html)
        self.assertNotIn("条记录", html)


class GenerationProgressMessageTests(unittest.TestCase):
    def test_unknown_tunnel_reuses_runtime_name(self) -> None:
        self.assertEqual(
            generation_progress_message("single_tunnel", "  新增测试隧道  "),
            "新增测试隧道：单隧道月报表生成完成",
        )

    def test_known_display_name_mapping_is_applied(self) -> None:
        self.assertEqual(
            generation_progress_message("fault_record", "小湖坳隧道"),
            "遂川小湖坳隧道：设备故障记录单生成完成",
        )

    def test_total_message_has_no_tunnel_prefix(self) -> None:
        self.assertEqual(generation_progress_message("total"), "总月报表生成完成")


if __name__ == "__main__":
    unittest.main()

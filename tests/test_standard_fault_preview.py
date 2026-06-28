from __future__ import annotations

import unittest

import pandas as pd

from core.repair_orders.preview import build_trace_rows, visible_preview_columns
from core.repair_orders.quality import row_label


class StandardFaultPreviewTests(unittest.TestCase):
    def test_visible_preview_columns_keep_known_order(self) -> None:
        data = pd.DataFrame(
            columns=[
                "设备名称",
                "源表行号",
                "原因及处理",
                "未展示字段",
                "隧道名称",
            ]
        )

        self.assertEqual(visible_preview_columns(data), ["源表行号", "隧道名称", "设备名称", "原因及处理"])

    def test_trace_rows_explain_key_fields(self) -> None:
        row = pd.Series(
            {
                "故障现象": "摄像机离线",
                "处置措施": "重启后恢复",
                "原因及处理": "通信中断，重启后恢复",
                "故障地点": "YK12+345",
            }
        )

        fields = [item["字段"] for item in build_trace_rows(row)]

        self.assertEqual(fields, ["故障现象", "处置措施", "原因及处理", "故障地点"])

    def test_row_label_uses_source_row_when_present(self) -> None:
        row = pd.Series({"源表行号": "12.0", "隧道名称": "测试隧道", "设备名称": "摄像机", "故障日期": "2026-07-01"})

        self.assertEqual(row_label(row, 0), "12 | 测试隧道 | 摄像机 | 2026-07-01")


if __name__ == "__main__":
    unittest.main()

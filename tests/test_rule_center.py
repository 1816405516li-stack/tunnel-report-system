from __future__ import annotations

import unittest

from pages.components.panels.rule_center import RULE_LABELS


class RuleCenterLabelTests(unittest.TestCase):
    def test_single_tunnel_report_name_is_canonical(self) -> None:
        labels = "\n".join(RULE_LABELS.values())
        self.assertIn("机电设施故障月报表（分隧道表）", labels)
        self.assertNotIn("机电故障月报表（分隧道设施表）", labels)
        self.assertNotIn("分隧道设施表", labels)


if __name__ == "__main__":
    unittest.main()

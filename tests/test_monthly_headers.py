from __future__ import annotations

import unittest

from generators.monthly_reports.single_tunnel import HEADER_GAP as SINGLE_TUNNEL_HEADER_GAP
from generators.monthly_reports.total import HEADER_GAP as TOTAL_HEADER_GAP


class MonthlyHeaderTests(unittest.TestCase):
    def test_header_gap_uses_stable_full_width_spaces(self) -> None:
        self.assertEqual(TOTAL_HEADER_GAP, "\u3000" * 7)
        self.assertEqual(SINGLE_TUNNEL_HEADER_GAP, "\u3000" * 7)


if __name__ == "__main__":
    unittest.main()

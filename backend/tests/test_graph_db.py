import os
import unittest
from state.graph_db import GraphDatabase

class TestGraphDatabase(unittest.TestCase):
    def setUp(self):

        self.test_db_path = "test_graph.db"
        self.db = GraphDatabase(self.test_db_path)

    def tearDown(self):

        self.db.clear()

        if os.path.exists(self.test_db_path):
            try:
                os.remove(self.test_db_path)
            except PermissionError:
                pass

    def test_add_and_retrieve_node(self):
        self.db.add_node("wb_1", "Workbook", {"name": "Sales.xlsx"})
        node = self.db.get_node("wb_1")
        self.assertIsNotNone(node)
        self.assertEqual(node[0], "wb_1")
        self.assertEqual(node[1], "Workbook")
        self.assertEqual(node[2]["name"], "Sales.xlsx")

    def test_add_edge_and_neighbors(self):
        self.db.add_node("wb_1", "Workbook", {"name": "Sales.xlsx"})
        self.db.add_node("sheet_1", "Sheet", {"name": "Q1"})
        self.db.add_edge("wb_1", "sheet_1", "HAS_SHEET", {"created_at": "2026-06-15"})

        neighbors = self.db.get_neighbors("wb_1")
        self.assertEqual(len(neighbors), 1)
        self.assertEqual(neighbors[0][0], "sheet_1")
        self.assertEqual(neighbors[0][1], "Sheet")
        self.assertEqual(neighbors[0][3]["created_at"], "2026-06-15")

    def test_cascade_delete(self):
        self.db.add_node("wb_1", "Workbook", {"name": "Sales.xlsx"})
        self.db.add_node("sheet_1", "Sheet", {"name": "Q1"})
        self.db.add_edge("wb_1", "sheet_1", "HAS_SHEET")

        summary_before = self.db.get_summary()
        self.assertEqual(len(summary_before["edges"]), 1)




        self.db.clear()
        summary_after = self.db.get_summary()
        self.assertEqual(len(summary_after["nodes"]), 0)
        self.assertEqual(len(summary_after["edges"]), 0)

if __name__ == '__main__':
    unittest.main()
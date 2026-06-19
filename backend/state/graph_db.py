import sqlite3
import json
import os
from typing import Dict, Any, List, Tuple

class GraphDatabase:
    """
    A lightweight property graph database implemented on top of SQLite.
    Stores nodes and edges with arbitrary JSON properties.
    """
    def __init__(self, db_path: str = "xl_mcp_graph.db") -> None:
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS nodes (
                    id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    properties TEXT NOT NULL
                );
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS edges (
                    source_id TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    type TEXT NOT NULL,
                    properties TEXT NOT NULL,
                    PRIMARY KEY (source_id, target_id, type),
                    FOREIGN KEY (source_id) REFERENCES nodes(id) ON DELETE CASCADE,
                    FOREIGN KEY (target_id) REFERENCES nodes(id) ON DELETE CASCADE
                );
            """)
            conn.commit()

    def add_node(self, id: str, type: str, properties: Dict[str, Any]) -> None:
        props_str = json.dumps(properties)
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO nodes (id, type, properties) VALUES (?, ?, ?) "
                "ON CONFLICT(id) DO UPDATE SET type=excluded.type, properties=excluded.properties;",
                (id, type, props_str)
            )
            conn.commit()

    def add_edge(self, source_id: str, target_id: str, type: str, properties: Dict[str, Any] = None) -> None:
        props = properties or {}
        props_str = json.dumps(props)
        with self._get_connection() as conn:
            try:
                conn.execute(
                    "INSERT INTO edges (source_id, target_id, type, properties) VALUES (?, ?, ?, ?) "
                    "ON CONFLICT(source_id, target_id, type) DO UPDATE SET properties=excluded.properties;",
                    (source_id, target_id, type, props_str)
                )
                conn.commit()
            except sqlite3.IntegrityError as e:

                pass

    def get_node(self, id: str) -> Tuple[str, str, Dict[str, Any]] or None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, type, properties FROM nodes WHERE id = ?;", (id,))
            row = cursor.fetchone()
            if row:
                return row[0], row[1], json.loads(row[2])
            return None

    def get_neighbors(self, node_id: str, edge_type: str = None) -> List[Tuple[str, str, Dict[str, Any], Dict[str, Any]]]:
        query = """
            SELECT n.id, n.type, n.properties, e.properties
            FROM edges e
            JOIN nodes n ON e.target_id = n.id
            WHERE e.source_id = ?
        """
        params = [node_id]
        if edge_type:
            query += " AND e.type = ?"
            params.append(edge_type)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [(row[0], row[1], json.loads(row[2]), json.loads(row[3])) for row in rows]

    def get_summary(self) -> Dict[str, Any]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, type, properties FROM nodes;")
            nodes = [{"id": r[0], "type": r[1], "properties": json.loads(r[2])} for r in cursor.fetchall()]

            cursor.execute("SELECT source_id, target_id, type, properties FROM edges;")
            edges = [{"source": r[0], "target": r[1], "type": r[2], "properties": json.loads(r[3])} for r in cursor.fetchall()]

            return {"nodes": nodes, "edges": edges}

    def clear(self) -> None:
        with self._get_connection() as conn:
            conn.execute("DELETE FROM edges;")
            conn.execute("DELETE FROM nodes;")
            conn.commit()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "xl_mcp_graph.db")
graph_db = GraphDatabase(db_path)
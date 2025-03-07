# src from here --------------------------------------------------------------------------------
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# # Time-stamp: "2024-11-24 22:30:57 (ywatanabe)"
# # File: ./mngs_repo/src/mngs/db/_PostgreSQL_modules/_QueryMixin.py
# 
# __file__ = "/home/ywatanabe/proj/mngs_repo/src/mngs/db/_PostgreSQL_modules/_QueryMixin.py"
# 
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# 
# from typing import List, Dict, Any, Optional, Union, Tuple
# from .._BaseMixins._BaseQueryMixin import _BaseQueryMixin
# 
# class _QueryMixin(_BaseQueryMixin):
#     def select(self, table: str, columns: Optional[List[str]] = None, where: Optional[str] = None,
#                params: Optional[tuple] = None, order_by: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
#         """Execute a SELECT query with optional conditions"""
#         cols_str = "*" if not columns else ", ".join(columns)
#         query = f"SELECT {cols_str} FROM {table}"
# 
#         if where:
#             query += f" WHERE {where}"
#         if order_by:
#             query += f" ORDER BY {order_by}"
#         if limit:
#             query += f" LIMIT {limit}"
# 
#         self.execute(query, params)
#         columns = [desc[0] for desc in self.cursor.description]
#         return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
# 
#     def insert(self, table: str, data: Dict[str, Any]) -> None:
#         """Insert a single record into a table"""
#         self._check_writable()
#         columns = list(data.keys())
#         values = list(data.values())
#         placeholders = ["%s"] * len(values)
# 
#         query = f"""
#             INSERT INTO {table}
#             ({', '.join(columns)})
#             VALUES ({', '.join(placeholders)})
#         """
# 
#         self.execute(query, tuple(values))
# 
#     def update(self, table: str, data: Dict[str, Any], where: str, params: Optional[tuple] = None) -> int:
#         """Update records in a table"""
#         self._check_writable()
#         set_items = [f"{k} = %s" for k in data.keys()]
#         values = list(data.values())
# 
#         query = f"""
#             UPDATE {table}
#             SET {', '.join(set_items)}
#             WHERE {where}
#         """
# 
#         if params:
#             values.extend(params)
# 
#         self.execute(query, tuple(values))
#         return self.cursor.rowcount
# 
#     def delete(self, table: str, where: str, params: Optional[tuple] = None) -> int:
#         """Delete records from a table"""
#         self._check_writable()
#         query = f"DELETE FROM {table} WHERE {where}"
#         self.execute(query, params)
#         return self.cursor.rowcount
# 
#     def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
#         """Execute a custom query and return results as dictionaries"""
#         self.execute(query, params)
# 
#         if self.cursor.description:  # If the query returns results
#             columns = [desc[0] for desc in self.cursor.description]
#             return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
#         return []
# 
#     def count(self, table: str, where: Optional[str] = None, params: Optional[tuple] = None) -> int:
#         """Count records in a table"""
#         query = f"SELECT COUNT(*) FROM {table}"
#         if where:
#             query += f" WHERE {where}"
# 
#         self.execute(query, params)
#         return self.cursor.fetchone()[0]
# 
# 
# # EOF

# test from here --------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
import pytest
import numpy as np

# Add project root to Python path
project_root = str(Path(__file__).parent.parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, os.path.join(project_root, "src"))

from mngs..db._PostgreSQLMixins._QueryMixin import *

class Test_MainFunctionality:
    def setup_method(self):
        # Setup test fixtures
        pass

    def teardown_method(self):
        # Clean up after tests
        pass

    def test_basic_functionality(self):
        # Basic test case
        pass

    def test_edge_cases(self):
        # Edge case testing
        pass

    def test_error_handling(self):
        # Error handling testing
        pass

# src from here --------------------------------------------------------------------------------
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# # Time-stamp: "2024-11-24 22:11:37 (ywatanabe)"
# # File: ./mngs_repo/src/mngs/db/_PostgreSQL_modules/_BatchMixin.py
# 
# __file__ = "/home/ywatanabe/proj/mngs_repo/src/mngs/db/_PostgreSQL_modules/_BatchMixin.py"
# 
# from typing import List, Any, Optional, Dict, Union
# import pandas as pd
# from .._BaseMixins._BaseBatchMixin import _BaseBatchMixin
# 
# class _BatchMixin(_BaseBatchMixin):
#     def insert_many(self, table: str, records: List[Dict[str, Any]], batch_size: Optional[int] = None) -> None:
#         if not records:
#             return
# 
#         query = self._prepare_insert_query(table, records[0])
#         if batch_size and batch_size > 0:
#             for i in range(0, len(records), batch_size):
#                 batch = records[i:i + batch_size]
#                 parameters = self._prepare_batch_parameters(batch)
#                 self.executemany(query, parameters)
#         else:
#             parameters = self._prepare_batch_parameters(records)
#             self.executemany(query, parameters)
# 
#     def _prepare_insert_query(self, table: str, record: Dict[str, Any]) -> str:
#         columns = list(record.keys())
#         placeholders = ["%s"] * len(columns)
#         columns_str = ", ".join(columns)
#         placeholders_str = ", ".join(placeholders)
#         return f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders_str})"
# 
#     def _prepare_batch_parameters(self, records: List[Dict[str, Any]]) -> List[tuple]:
#         if not records:
#             return []
# 
#         columns = list(records[0].keys())
#         return [tuple(record[col] for col in columns) for record in records]
# 
#     def dataframe_to_sql(self, df: pd.DataFrame, table: str, if_exists: str = 'fail') -> None:
#         if if_exists not in ['fail', 'replace', 'append']:
#             raise ValueError("if_exists must be one of 'fail', 'replace', or 'append'")
# 
#         if if_exists == 'replace':
#             self.execute(f"DROP TABLE IF EXISTS {table}")
#             # Create table based on DataFrame schema
#             columns = []
#             for col, dtype in df.dtypes.items():
#                 pg_type = self._map_dtype_to_postgres(dtype)
#                 columns.append(f"{col} {pg_type}")
#             columns_str = ", ".join(columns)
#             self.execute(f"CREATE TABLE {table} ({columns_str})")
# 
#         records = df.to_dict('records')
#         self.insert_many(table, records)
# 
#     def _map_dtype_to_postgres(self, dtype) -> str:
#         dtype_str = str(dtype)
#         if 'int' in dtype_str:
#             return 'INTEGER'
#         elif 'float' in dtype_str:
#             return 'REAL'
#         elif 'datetime' in dtype_str:
#             return 'TIMESTAMP'
#         elif 'bool' in dtype_str:
#             return 'BOOLEAN'
#         else:
#             return 'TEXT'
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

from mngs..db._PostgreSQLMixins._BatchMixin import *

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

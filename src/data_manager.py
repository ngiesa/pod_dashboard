from datetime import date

import pandas as pd


# from conn.hdl.data_manager import DashDataManager
#
class DummyDataManager:
    """Dummy data manager for testing purposes"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def get_last_updated(self):
        return "01.01.2024"

    def get_dropdown_items(self, pream_col):
        return [{"label": "dummy", "value": "dummy"}]

    def get_date_items(self):
        """Minimal and maximum data"""
        return [date(2020, 1, 1), date(2024, 1, 1)]

    def filter_main_table(self, filter_condition):
        return pd.DataFrame(
            {
                "RISK": [0.9, 0.1, 1.0, 0.2],
                "COPID": [0, 1, 2, 3],
                "BEGANORG": [0, 1, 2, 3],
                "ENDANORG": [1, 2, 3, 4],
                "OTHER": [3, 1, 4, 5],
            }
        )

    def reset_filter(self):
        return pd.DataFrame(
            {
                "RISK": [0.9, 0.1, 1.0, 0.2],
                "COPID": [0, 1, 2, 3],
                "BEGANORG": [0, 1, 2, 3],
                "ENDANORG": [1, 2, 3, 4],
                "OTHER": [3, 1, 4, 5],
            }
        )

    def display_master_table(self):
        return pd.DataFrame(
            {
                "RISK": [90.0],
                "COPID": [0, 1, 2, 3],
                "BEGANORG": [0, 1, 2, 3],
                "ENDANORG": [1, 2, 3, 4],
                "OTHER": [3, 1, 4, 5],
            }
        )

    def data_op_master(self):
        return []

    def get_vitals(self, c_root, c_begin, c_end):
        return []


ddm = DummyDataManager()

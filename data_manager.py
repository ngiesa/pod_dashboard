
import pandas as pd
from conn.hdl.utils import get_var_df, open_var_ids
from random import random

class DashDataManager():
    
    def __init__(self):
        print("init data manager")
        self.var_df = get_var_df(open_var_ids())
        # defines variables that should be displayed
        self.prem_items = ["prem_sex", "prem_age","prem_opward", "prem_org_unit", "prem_area", 
                           "prem_org_name", "prem_dia_main", "prem_anes"]
        self.vitals_items = ["vital_puls", "vital_spo2", "vital_nipb", "vital_ipb", "vital_rr", "vital_tmp", "vital_hr"]
        self.display_main_items = ["prem_sex", "prem_age", "prem_anes", "prem_opward", "prem_org_name"]
        # defines time related columns that were shortened on display
        self.TIME_COLS = ["BEGAN", "ENDAN", "BEGAW", "ENDAW"]
        # storing all filters that are applied to data
        self.all_filter_conditions = {}
        self.load_data()
        self.prepare_items()
        
    def load_data(self):
        """ loads data """
        self.data_op_master = pd.read_csv("./conn/hdl/data/data_op_master.csv", index_col=0, low_memory=False)
        self.df_premed = pd.read_csv("./conn/hdl/data/data_premed.csv", index_col=0, low_memory=False)
        self.df_vital = pd.read_csv("./conn/hdl/data/data_vital.csv", index_col=0, low_memory=False)
        
    def get_last_updated(self):
        """ gets last entry in op master table """
        last_update = self.reset_filter().sort_values(["DATE","BEGAN"], ascending=False).iloc[0]
        return "{} {}".format(last_update["DATE"], last_update["BEGAN"])
        
    def prepare_items(self):
        """ prepares premed data """
        max_version = self.df_premed.groupby(["c_op_id", "c_var_id"])\
            ["c_version"].max().reset_index().drop_duplicates()
        df_premed_main = self.df_premed.merge(max_version, on=["c_op_id", "c_var_id", "c_version"], how="inner")
        df_premed_main = df_premed_main.drop(columns=["c_date_time_to", "c_id"])\
            .drop_duplicates().merge(self.var_df[self.var_df.var_name.isin(self.prem_items)],
                on="c_var_id", suffixes=["_", ""]).dropna().\
                    pivot(index=['c_op_id'], 
                            columns='var_name',
                            values="c_val").reset_index()
        self.df_premed_main = df_premed_main
        
    def get_display_times(self, df):
        """ converts time stamps """
        df.loc[:, "DATE"] = [str(s)[0:10] for s in df["BEGAN"]]
        for i, col in enumerate(self.TIME_COLS):
            df.loc[:, col + "_ORG"] = df[col]
            df.loc[:, col] = [str(s)[-8:-3] for s in df[col]]
        return df

    def get_display_main_table(self, df_main):
        """ gets display main table """
        df_main = self.get_display_times(df_main)
        df_main = df_main[["c_op_id", "DATE"] + self.TIME_COLS + self.display_main_items + [c + "_ORG" for c in self.TIME_COLS]]
        columns = [x.replace("prem_", "").replace("_", "").upper() for x in df_main.columns]
        df_main.columns = columns
        #TODO REPLACE WITH REAL PREDICTIONS
        PRED = [round(random(), 2) for _ in range(0, len(df_main))]
        df_main['RISK'] = PRED
        df_main['CONFID'] = ["({},{})".format(str(round(p-0.02,2)), \
            str(round(p+0.02,2))) for p in PRED]
        self.display_master_table = df_main.sort_values(["DATE", "BEGAN"], ascending=False)
        return self.display_master_table
    
    def filter_main_table(self, filter_map = {"item1": {"variable": "prem_sex", "value": "male", "condition": "equal"}}):
        """ applied sets of filter items to main table """
        df_premed_filter = self.df_premed_main
        df_premed_filter["prem_age"] = pd.to_numeric(df_premed_filter["prem_age"])
        if len(list(filter_map.keys())) != 0:
            key = list(filter_map.keys())[0]
            self.all_filter_conditions[key] = filter_map[key] #TODO STORE ALL FILTER CONDITIONS
        df_main = self.data_op_master.merge(df_premed_filter, on="c_op_id")
        for k in self.all_filter_conditions.keys():
            item = self.all_filter_conditions[k]
            print(item)
            if item["condition"] == "equal":
                if item["value"] is not None:
                    df_main = df_main[df_main[item["variable"]] == item["value"]]
            if item["condition"] == "greater":
                if item["value"] is not None:
                    df_main = df_main[df_main[item["variable"]] > item["value"]]
            if item["condition"] == "less":
                if item["value"] is not None:
                    df_main = df_main[df_main[item["variable"]] < item["value"]]
        return self.get_display_main_table(df_main=df_main)
    
    
    def reset_filter(self):
        """ reset filters and get display table """
        df_display = self.filter_main_table(filter_map={}).sort_values(["DATE", "BEGAN"], ascending=False)
        return df_display
    
    def resample_display_time(self, df):
        """ group time by minutes and not by milliseconds """
        assert ("c_date_time_to" in list(df.columns)) & ("c_val" in list(df.columns))
        return df\
                .assign(c_time = [pd.to_datetime(t[0:16]) for t in df.c_date_time_to])\
                .assign(c_value = pd.to_numeric(df.c_val))
    
    def get_vitals(self, c_root="", c_begin="", c_end=""):
        """ filter to vital signs per root identifier """
        # reduce vital results to root ids and begin end
        df_vital = self.df_vital
        df_vital_display = df_vital[(df_vital.c_root_id == c_root) 
         & (df_vital.c_date_time_to >= c_begin) 
         & (df_vital.c_date_time_to <= c_end)]\
             .merge(self.var_df[self.var_df.var_name.isin(self.vitals_items)], on="c_var_id")
        print("print available variable names")
        print(df_vital_display.var_name.drop_duplicates())
        # get suffix indicators
        df_vital_display = df_vital_display\
            .assign(var_name = df_vital_display.var_name + df_vital_display.c_suffix.fillna(""))
        df_vital_display = self.resample_display_time(df_vital_display)
        # return table
        return df_vital_display
    
    def get_dropdown_items(self, pream_col):
        print("GET DROPDOWN ITEMS")# TODO Implement conditional filtering
        """ return all possible values for the clinical unit"""
        assert pream_col in list(self.df_premed_main.columns)
        return [{'label': i, 'value': i} 
                for i in self.df_premed_main[pream_col].drop_duplicates().dropna()]
        
    def get_date_items(self):
        """ read the min and max timestamps of surgery master table """
        return pd.to_datetime(self.data_op_master["BEGAN"].min()), \
                pd.to_datetime(self.data_op_master["BEGAN"].max())
        
            
        

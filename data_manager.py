
import pandas as pd
from conn.hdl.utils import get_var_df, open_var_ids
from random import random
from conn.hdl.db_connector import DBConnector
from conn.hdl.utils import parse_sql_file

class DashDataManager():
    
    def __init__(self, engine = {}):
        print("init data manager")
        self.engine = DBConnector(user="giesan", psw="2020Hamster", target_db="hdl", extract_date="\"01/01/2024\"").engine
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
        self.filter_menu = None
        self.display_master_table = None
        self.pod_revalence = 0
        self.get_last_updated()
        self.load_data(to_dt=self.max_timestamp.astype(str)[0], 
                        from_dt=(self.max_timestamp - pd.Timedelta(days=7))\
                        .astype(str)[0])
        
    def load_data(self, from_dt, to_dt):
        """ loads data """
        print("loading data") #TODO LIMIT THE DATA RECORDS BUT MAP ALSO VITAL SIGNS TODO CURENTLY SELECTED OP IDS STORE!!s
        if (from_dt == "NaT") or (to_dt == "NaT"):
            print(to_dt)
            print("NAT")
        # check if initial load 
        print(parse_sql_file("./conn/hdl/sql/sql_dm_op_select.sql").format(to_dt, from_dt))
        self.df_op_master = pd.read_sql(parse_sql_file("./conn/hdl/sql/sql_dm_op_select.sql").format(to_dt, from_dt), con=self.engine)
        print(len(self.df_op_master))
        self.min_date = pd.to_datetime(self.df_op_master["BEGAN"]).max()
        self.max_date = pd.to_datetime(self.df_op_master["BEGAN"]).max()
        self.df_premed = pd.read_sql("SELECT * FROM data_preamed WHERE c_op_id IN ('{}')"\
            .format("\',\'".join(list(self.df_op_master.c_op_id))), con=self.engine).drop(columns="hash_check") 
        self.df_nudesc = pd.read_sql("SELECT * FROM data_nudesc WHERE c_root_id IN ('{}')"\
            .format("\',\'".join(list(self.df_op_master.c_root_id))), con=self.engine).drop(columns="hash_check") 
        self.prepare_items()
        self.prepared_nudesc()
    
    def prepared_nudesc(self):
        """ prepare nudesc display data also for line chart """
        df_nudesc_master = self.df_op_master.merge(self.df_nudesc[["c_nudesc", "c_nu_timestamp", "c_version", "c_root_id"]], on="c_root_id", how="left")
        df_nudesc_master = df_nudesc_master[((df_nudesc_master.c_nu_timestamp > df_nudesc_master["BEGAN"]) &\
            (df_nudesc_master.c_nu_timestamp < df_nudesc_master["ENDAW"])) | (df_nudesc_master.c_nudesc.isna())]
        df_nudesc_master = df_nudesc_master.groupby(["BEGAN", "c_op_id", "c_root_id"])["c_nudesc"].max().reset_index()
        df_nudesc_master = df_nudesc_master.assign(day = [str(t)[0:10] for t in df_nudesc_master["BEGAN"]])
        df_nudesc_master = df_nudesc_master.assign(pod = ["yes" if x > 0 else "no" if x == 0 else "NaN" for x in df_nudesc_master.c_nudesc])
        if "pod" in self.df_op_master.columns:
            self.df_op_master = self.df_op_master.drop(columns=["pod"])
        self.df_op_master = self.df_op_master.merge(df_nudesc_master[["c_op_id", "pod"]], on="c_op_id")
        print("pod columns")
        print(self.df_op_master.columns)
        if any(x == "yes" for x in df_nudesc_master.pod):
            self.pod_revalence = round(list(df_nudesc_master.pod).count("yes")/\
            (list(df_nudesc_master.pod).count("no")+list(df_nudesc_master.pod).count("yes"))*100, 2)
        self.df_nudesc_master = df_nudesc_master
        
        
    def get_last_updated(self):
        """ gets last entry in op master table """
        self.max_timestamp = pd.to_datetime(pd.read_sql("SELECT MAX(c_start) FROM data_op_master", con=self.engine).iloc[0])
        return self.max_timestamp.astype(str)
        
    def prepare_items(self):
        """ prepares premed data """
        max_version = self.df_premed.groupby(["c_op_id", "c_var_id"])["c_version"].max().reset_index().drop_duplicates()
        df_premed_main = self.df_premed.merge(max_version, on=["c_op_id", "c_var_id", "c_version"], how="inner")
        df_premed_main = df_premed_main.drop(columns=["c_date_time_to", "c_id"])\
            .drop_duplicates().merge(self.var_df[self.var_df.var_name.isin(self.prem_items)],
                on="c_var_id", suffixes=["_", ""]).dropna().\
                    pivot(index=['c_op_id'], 
                            columns='var_name',
                            values="c_val").reset_index()
        #TODO age not always assigned?
        print(df_premed_main.columns)
        df_premed_main["prem_age"] = pd.to_numeric(df_premed_main["prem_age"])
        self.df_premed_main = df_premed_main
        
    def get_display_times(self, df):
        """ converts time stamps """
        df.loc[:, "DATE"] = [str(s)[0:10] for s in df["BEGAN"]]
        for i, col in enumerate(self.TIME_COLS):
            df.loc[:, col + "_ORG"] = df[col]
            df.loc[:, col] = [str(s)[10:16] if str(s)[0:5] == str(df["DATE"].iloc[i])[0:5]\
                else str(s)[10:16]+"+1Day" for i, s in enumerate(df[col])]       
        return df

    def get_display_main_table(self, df_main):
        """ gets display main table """
        df_main = self.get_display_times(df_main)
        if "pod" in df_main.columns:
            df_main["POD"] = df_main.pod
        df_main = df_main[["c_op_id", "DATE"] + self.TIME_COLS + self.display_main_items + [c + "_ORG" for c in self.TIME_COLS] + ["POD"]]
        columns = [x.replace("prem_", "").replace("_", "").upper() for x in df_main.columns]
        df_main.columns = [c.upper() for c in columns]
        #TODO REPLACE WITH REAL PREDICTIONS
        PRED = [round(random(), 2) for _ in range(0, len(df_main))]
        df_main['RISK'] = PRED
        df_main['CONFID'] = ["({},{})".format(str(round(p-0.02,2)), \
            str(round(p+0.02,2))) for p in PRED]
        self.display_master_table = df_main.sort_values(["DATE", "BEGAN"], ascending=False)
        print("display main table: ", len(self.display_master_table))
        return self.display_master_table
    
    def filter_main_table(self, filter_map = {}): #TODO FILTER THESE DATA WITH SQL QUERY!
        """ applied sets of filter items to main table """
        if len(list(filter_map.keys())) != 0:
            key = list(filter_map.keys())[0]
            self.all_filter_conditions[key] = filter_map[key] #TODO STORE ALL FILTER CONDITIONS
        df_premed_filter = self.df_premed_main
        df_main = self.df_op_master.merge(df_premed_filter, on="c_op_id")
        # handle times filtering as base for filters 
        began_items = [filter_map[item] for item in filter_map if filter_map[item]['variable'] == 'BEGAN']
        if len(began_items) > 0:
            item = began_items[0]
            print(item)
            if item['condition'] == 'greater':
                print(self.df_op_master["BEGAN"])
                print(self.df_op_master.empty)
                if str(pd.to_datetime(self.df_op_master["BEGAN"]).max()) < item['value'].replace("T", " ") + " 00:00:00":
                    return self.display_master_table
                self.load_data(from_dt=item['value'].replace("T", " ") + " 00:00:00", 
                            to_dt=str(pd.to_datetime(self.df_op_master["BEGAN"]).max())) #TODO FROM AND TO IS CHANGED??
            if item['condition'] == 'less':
                if str(pd.to_datetime(self.df_op_master["BEGAN"]).min()) > item['value'].replace("T", " ") + " 00:00:00":
                    return self.display_master_table
                self.load_data(to_dt=item['value'].replace("T", " ") + " 23:00:00", 
                            from_dt=str(pd.to_datetime(self.df_op_master["BEGAN"]).min())) #TODO FROM AND TO IS CHANGED??
            # get new df main table with updated df_op_master
            df_premed_filter = self.df_premed_main
            df_main = self.df_op_master.merge(df_premed_filter, on="c_op_id")
        
        for k in self.all_filter_conditions.keys():
            item = self.all_filter_conditions[k]
            print("filter data")
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
        return self.get_display_main_table(df_main=df_main) #IF POD IN COLS UPPER CASE POD
    
    
    def reset_filter(self):
        """ reset filters and get display table """ #TODO CUTS THE MASTER TABLE
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
        df_vital = pd.read_sql("SELECT * FROM data_vital WHERE c_root_id IN ('{}')"\
            .format(c_root), con=self.engine).drop(columns="hash_check")
        df_vital_display = df_vital[(df_vital.c_date_time_to.astype(str) >= str(c_begin)) \
            & (df_vital.c_date_time_to.astype(str) <= str(c_end))]\
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
        print("GET DROPDOWN ITEMS") #TODO UPDATE ACTIVELY DROP DOWNS OF DISPLAY ITEM!! TODO IMPLEMENT THE STATISTICS PAGE WITH FILTERS!!
        """ return all possible values for the clinical unit"""
        assert pream_col in list(self.df_premed_main.columns)
        return [{'label': i, 'value': i} 
                for i in self.df_premed_main[pream_col].drop_duplicates().dropna()]
        
    def get_date_items(self):
        """ read the min and max timestamps of surgery master table """
        return pd.to_datetime(self.df_op_master["BEGAN"].min()), \
                pd.to_datetime(self.df_op_master["BEGAN"].max())

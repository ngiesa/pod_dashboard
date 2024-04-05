import json

import pandas as pd


def open_var_ids():
    """ open var id json """
    with open("./conn/hdl/var_ids.json", "r") as f:
        return json.load(f)


def get_var_df(var_ids):
    """ make var df from vars"""
    vars, ids = [], []
    for va in var_ids.keys():
        id = var_ids[va].split(",")
        vars = vars + len(id) * [va]
        ids = ids + id
    return pd.DataFrame({"var_name": vars, "c_var_id": [int(i) for i in ids]})


def listify_var_ids(var_ids):
    """ creates list from var id json """
    var_list = []
    for k in var_ids.keys():
        var_list.append(var_ids[k].replace(" ", ""))
    return var_list

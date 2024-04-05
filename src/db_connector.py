import hashlib

import jaydebeapi
from conn.hdl.utils import get_var_df, listify_var_ids, open_var_ids


class DBConnector:
    def __init__(
        self, user: str = "", psw: str = "", target_db: str = "hdl", extract_date=None
    ):
        """ configures connection to hdl, copra6, dash db """
        assert (user != "") and (psw != "") and (extract_date)
        assert target_db in ["hdl", "dash", "co6"]
        self.user = user
        self.psw = psw
        self.target_db = target_db
        self.conn = {}
        self.establish_conn()

    def establish_conn(self):
        """ call connect functions """
        if self.target_db == "hdl":
            self.conn = self.configure_hdl_connection()
            print("connected ")
        self.var_ids = open_var_ids()
        self.list_var_ids = listify_var_ids(self.var_ids)

    def configure_hdl_connection(self):
        """ sets hdl connection parameters """
        hdl_url = "jdbc:impala://hdl-edge01.charite.de:21057/default;AuthMech=3;SSL=1;CAIssuedCertNamesMismatch=1;AllowSelfSignedCerts=1"
        driver = "com.cloudera.impala.jdbc.Driver"
        jar_file = "./conn/hdl/ImpalaJDBC42.jar"
        conn = jaydebeapi.connect(driver, hdl_url, [self.user, self.psw], jar_file)
        return conn

    def parse_sql_file(self, path):
        """ opens and parses sql file """
        fd, sql = open(path, "r"), ""
        for s in fd:
            sql = sql + " " + s
        return sql

    def split_in_items(self, items: list = [], id=""):
        """ splits list of items for in clause """
        res = []
        for i in range(0, int(len(items.unique()) / 1000) + 1):
            res.append(",".join(items.unique()[i * 1000 : i * 1000 + 1000]))
        return ") OR {} IN (".format(id).join(res).replace("(,", "(")

    def hash_id_columns(self, df=None):
        """ hashes id columns in df """
        hash_cols = [x for x in df.columns if ("_id" in x) and (not "var" in x)]
        for col in hash_cols:
            df[col] = [
                hashlib.sha256(("" + str(v)).encode("utf-8")).hexdigest()
                for v in df[col]
            ]
        return df

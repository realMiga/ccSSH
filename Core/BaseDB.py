import pymysql

from config import (
    DB_DATABASE,
    DB_HOST,
    DB_USER,
    DB_PASSWORD,
    DB_CHARSET
)


class DBResult:
    Suc = False
    Result = None
    Err = None
    Rows = None

    def __init__(self):
        pass


class BaseDB:
    def __init__(self):
        self.dbConn = None
        self.cursor = None

    # Return DBResult
    def select(self, sql, params=None):
        with pymysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_DATABASE, charset=DB_CHARSET,
                             cursorclass=pymysql.cursors.DictCursor) as cursor:

            r = DBResult()
            try:
                if params is None or len(params) == 0 or type(params) != dict:
                    r.Rows = cursor.execute(sql)
                else:
                    r.Rows = cursor.execute(sql, params)
                r.Result = cursor.fetchall() if r.Rows != 0 else []
                for i in range(0, len(r.Result)):
                    for k, v in r.Result[i].items():
                        r.Result[i][k] = str(v)
                r.Suc = True
            except Exception as e:
                r.Err = e


        return r

    # Return DBResult
    def callProc(self, func, params=None):
        with pymysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB, charset=DB_CHARSET,
                             cursorclass=pymysql.cursors.DictCursor) as cursor:
            r = DBResult()
            try:
                if params:
                    cursor.callproc(func, params)
                else:
                    cursor.callproc(func)
                r.Result = cursor.fetchall()
                r.Suc = True
            except Exception as e:
                r.Err = e


        return r

    # Return DBResult
    def execute(self, sql, params=None):
        self.dbConn = pymysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB,
                                      charset=DB_CHARSET,
                                      cursorclass=pymysql.cursors.DictCursor)
        with pymysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB, charset=DB_CHARSET,
                             cursorclass=pymysql.cursors.DictCursor) as cursor:

            r = DBResult()
            try:
                if not params:
                    r.Rows = cursor.execute(sql)
                else:
                    r.Rows = cursor.execute(sql, params)
                r.Result = cursor.fetchall() if r.Rows != 0 else []
                r.Suc = True
                self.dbConn.commit()
            except Exception as e:
                r.Err = e
                print(e, 'execute Error')
                self.dbConn.rollback()


        try:
            self.dbConn.close()
        except:
            pass
        return r

    # Return DBResult
    def insert(self, sql, params=None):
        r = self.execute(sql, params)
        return r

    def getLastID(self):
        r = self.execute("SELECT LAST_INSERT_ID()")
        r.Result = r.Result[0]['LAST_INSERT_ID()']
        return r

    # Return DBResult
    def getValue(self, sql, params=None):
        r = self.select(sql, params)
        if r.Suc:
            if r.Result:
                r.Result = r.Result[0]
            else:
                r.Result = -1
        return r
